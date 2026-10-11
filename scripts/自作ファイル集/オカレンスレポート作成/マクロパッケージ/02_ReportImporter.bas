Attribute VB_Name = "ReportImporter"
Option Explicit

'=====================================================================
'  手術室オカレンス報告 自動振り分けマクロ（オフライン動作）
'
'  使い方：
'    1) Alt+F8 →「貼付エリア初期化」でシート「⑦貼付エリア」を作成
'    2) Excel/Word の表や本文をコピーし、⑦貼付エリアの A2 に貼り付け
'    3) Alt+F8 →「報告収集へ転記」を実行
'       → ⑥報告収集 の末尾に、日付・職種・部屋番号・分類・診療科・時間帯を自動振り分けして追記
'
'  自動処理内容：
'    - 対象年月(B列)  : ①基本入力の対象年 + 原文中の「M/D」から生成
'    - 職種(C列)      : 原文キーワードから 麻酔科/CE/NS を推定
'    - 部屋番号(E列)  : 「4room」「2A」「E9」等を抽出。複合表記(1room・消外・E9)にも対応
'    - 分類(F列)      : キーワード辞書で 確認不足・準備不足/機器/薬剤/コミュ/体制/その他 を自動割付
'    - 診療科(G列)    : 「消外」「整形」「心外」等を辞書で正規化
'    - 時間帯(H列)    : 「緊急」「時間外」「夜間」等の語を検出
'    - 備考(I列)      : 分類・職種の判定根拠キーワードを記録（レビュー用）
'
'  必要環境：Excel（マクロ有効ブック）のみ。ネット接続・追加参照不要。
'=====================================================================

Private Const PASTE_SHEET As String = "⑦貼付エリア"
Private Const TARGET_SHEET As String = "⑥報告収集"
Private Const BASE_SHEET As String = "①基本入力"

'=====================================================================
' シート「⑦貼付エリア」を初期化（無ければ作成、あれば内容クリア）
'=====================================================================
Public Sub 貼付エリア初期化()
    Dim ws As Worksheet
    Set ws = GetOrCreateSheet(PASTE_SHEET)

    Application.ScreenUpdating = False
    ws.Cells.Clear

    With ws
        .Range("A1").Value = "▼ ここから下（A2以降）に、Excel/Word の表や本文をそのまま貼り付けてください。1行=1報告 が理想。"
        .Range("A1").Font.Bold = True
        .Range("A1").Interior.Color = RGB(255, 242, 204)
        .Range("A1").Font.Color = RGB(120, 60, 0)

        .Range("C1").Value = "オプション"
        .Range("C1").Font.Bold = True
        .Range("D1").Value = "既定の職種（自動推定できないとき使用）："
        .Range("E1").Value = "自動推定"
        .Range("E1").Validation.Delete
        .Range("E1").Validation.Add Type:=xlValidateList, Formula1:="自動推定,麻酔科,CE,NS"

        .Range("F1").Value = "既定の時間帯："
        .Range("G1").Value = ""
        .Range("G1").Validation.Delete
        .Range("G1").Validation.Add Type:=xlValidateList, Formula1:=" ,午前（〜12時）,午後（12〜17時）,夕方（17〜19時）,夜間（19時〜）,緊急"

        .Columns("A").ColumnWidth = 90
        .Columns("B").ColumnWidth = 12
        .Columns("C:G").ColumnWidth = 20
        .Rows(1).RowHeight = 22

        ' 実行ボタンの案内
        .Range("A3").Value = "（貼り付け後、Alt+F8 →「報告収集へ転記」を実行）"
        .Range("A3").Font.Color = RGB(120, 120, 120)
        .Range("A3").Font.Italic = True

        .Activate
        .Range("A2").Select
    End With

    Application.ScreenUpdating = True
    MsgBox "「" & PASTE_SHEET & "」シートを準備しました。" & vbCrLf & "A2 以降に、Excel/Word の表や本文をそのまま貼り付けてください。" & vbCrLf & "貼り付けが済んだら Alt+F8 → 「報告収集へ転記」 を実行します。", vbInformation
End Sub

'=====================================================================
' メイン：⑦貼付エリアの内容を解析して ⑥報告収集 の末尾に追記
'=====================================================================
Public Sub 報告収集へ転記()
    Dim wsP As Worksheet, wsT As Worksheet, wsB As Worksheet
    On Error GoTo EH

    ' シート取得
    If Not SheetExists(PASTE_SHEET) Then
        If MsgBox("「" & PASTE_SHEET & "」シートがありません。今すぐ作成しますか？", vbYesNo + vbQuestion) = vbYes Then
            Call 貼付エリア初期化
        End If
        Exit Sub
    End If
    Set wsP = ThisWorkbook.Worksheets(PASTE_SHEET)
    Set wsT = ThisWorkbook.Worksheets(TARGET_SHEET)
    Set wsB = ThisWorkbook.Worksheets(BASE_SHEET)

    ' 対象年
    Dim baseYear As Long
    baseYear = CLng(NzNum(wsB.Range("B3").Value, Year(Date)))

    ' 既定職種・既定時間帯
    Dim defaultRole As String, defaultTime As String
    defaultRole = CStr(wsP.Range("E1").Value)
    If defaultRole = "自動推定" Or defaultRole = "" Then defaultRole = ""
    defaultTime = Trim$(CStr(wsP.Range("G1").Value))

    ' 貼付エリアの行数を判定
    Dim lastR As Long
    lastR = wsP.Cells(wsP.Rows.Count, "A").End(xlUp).Row
    If lastR < 2 Then
        MsgBox "貼付エリアが空です。A2 以降に貼り付けてから実行してください。", vbExclamation
        Exit Sub
    End If

    ' ⑥報告収集の書き込み開始行（D列の最終行の次）
    Dim wrRow As Long
    wrRow = wsT.Cells(wsT.Rows.Count, "D").End(xlUp).Row + 1
    If wrRow < 2 Then wrRow = 2

    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual

    Dim r As Long
    Dim addedCount As Long: addedCount = 0
    Dim skippedCount As Long: skippedCount = 0

    Dim rawA As String, rawB As String
    Dim mergedText As String

    For r = 2 To lastR
        rawA = CStr(wsP.Cells(r, 1).Value)
        rawB = CStr(wsP.Cells(r, 2).Value)

        ' 1つの報告として結合（A列単独 or A+B列）
        mergedText = Trim$(rawA)
        If Len(Trim$(rawB)) > 0 Then
            mergedText = mergedText & " " & Trim$(rawB)
        End If

        If Len(mergedText) < 5 Then
            skippedCount = skippedCount + 1
            GoTo NextRow
        End If

        ' 明らかな見出し行はスキップ
        If IsHeaderLine(mergedText) Then
            skippedCount = skippedCount + 1
            GoTo NextRow
        End If

        ' ---- 解析 ----
        Dim md As String   ' 「M/D」形式
        Dim yyyymm As String
        md = ExtractDate(mergedText)
        yyyymm = BuildYearMonth(baseYear, md)

        Dim roomStr As String, deptStr As String
        Call SplitRoomAndDept(mergedText, roomStr, deptStr)

        Dim roleStr As String, roleWhy As String
        roleStr = DetectRole(mergedText, roleWhy)
        If roleStr = "" Then roleStr = defaultRole

        Dim catStr As String, catWhy As String
        catStr = DetectCategory(mergedText, catWhy)

        Dim timeStr As String
        timeStr = DetectTimeSlot(mergedText)
        If timeStr = "" Then timeStr = defaultTime

        Dim noteStr As String
        noteStr = BuildNote(roleWhy, catWhy)

        ' ---- ⑥報告収集へ書き込み ----
        wsT.Cells(wrRow, 1).Formula = "=IF(D" & wrRow & "<>"""",ROW()-1,"""")"
        wsT.Cells(wrRow, 2).Value = yyyymm            ' 対象年月
        wsT.Cells(wrRow, 3).Value = roleStr           ' 職種
        wsT.Cells(wrRow, 4).Value = mergedText        ' 原文
        wsT.Cells(wrRow, 5).Value = roomStr           ' 部屋番号
        wsT.Cells(wrRow, 6).Value = catStr            ' 分類
        wsT.Cells(wrRow, 7).Value = deptStr           ' 診療科
        wsT.Cells(wrRow, 8).Value = timeStr           ' 時間帯
        wsT.Cells(wrRow, 9).Value = noteStr           ' 備考（判定根拠）

        ' 空欄セルに視覚的フラグ（薄い黄色）
        If Len(roleStr) = 0 Then wsT.Cells(wrRow, 3).Interior.Color = RGB(255, 255, 204)
        If Len(catStr) = 0 Then wsT.Cells(wrRow, 6).Interior.Color = RGB(255, 255, 204)

        wrRow = wrRow + 1
        addedCount = addedCount + 1
NextRow:
    Next r

    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True

    ' メッセージ
    Dim msg As String
    msg = addedCount & " 件を「" & TARGET_SHEET & "」に追記しました。" & vbCrLf
    If skippedCount > 0 Then msg = msg & "空行/見出し行として " & skippedCount & " 件をスキップしました。" & vbCrLf
    msg = msg & vbCrLf & "※ 職種・分類が推定できなかったセルは薄い黄色でハイライトしています。" & vbCrLf & "内容を確認し、必要に応じて手修正してください。" & vbCrLf & vbCrLf & "続けて「オカレンスレポート作成」を実行できます。"
    MsgBox msg, vbInformation

    ' 貼付エリアをクリアするか確認
    If MsgBox("「" & PASTE_SHEET & "」の内容をクリアしますか？", vbYesNo + vbQuestion) = vbYes Then
        wsP.Range("A2:B" & lastR).ClearContents
        wsP.Activate
        wsP.Range("A2").Select
    End If

    Exit Sub
EH:
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    MsgBox "エラーが発生しました：" & Err.Number & " " & Err.Description, vbCritical
End Sub

'=====================================================================
'                    以下、内部関数
'=====================================================================

'--- 見出し・区切り行判定 ---
Private Function IsHeaderLine(ByVal s As String) As Boolean
    Dim t As String
    t = Trim$(s)
    If Len(t) = 0 Then IsHeaderLine = True: Exit Function
    ' 表ヘッダ、区切り、記号のみ、ページ番号など
    If t = "No." Or t = "報告内容" Or t = "報告内容（原文）" Then IsHeaderLine = True: Exit Function
    If InStr(t, "オカレンスレポート報告") > 0 And Len(t) < 30 Then IsHeaderLine = True: Exit Function
    If Left$(t, 1) = "※" And Len(t) < 60 Then IsHeaderLine = True: Exit Function
    ' 「----」「======」等の区切り
    If Len(Replace(Replace(Replace(t, "-", ""), "=", ""), " ", "")) = 0 Then IsHeaderLine = True: Exit Function
    IsHeaderLine = False
End Function

'--- 日付抽出（M/D or M月D日） ---
Private Function ExtractDate(ByVal s As String) As String
    Dim i As Long, ch As String, buf As String
    Dim mm As Long, dd As Long
    Dim found As Boolean

    ' パターン1: M/D
    For i = 1 To Len(s) - 2
        ch = Mid$(s, i, 1)
        If IsNumeric(ch) Then
            ' 前が数字でない位置から開始
            If i > 1 Then
                If IsNumeric(Mid$(s, i - 1, 1)) Then GoTo NextI
            End If
            buf = ""
            Do While i <= Len(s) And IsNumeric(Mid$(s, i, 1))
                buf = buf & Mid$(s, i, 1)
                i = i + 1
                If Len(buf) >= 2 Then Exit Do
            Loop
            If i <= Len(s) Then
                If Mid$(s, i, 1) = "/" Then
                    mm = CLng(buf): buf = ""
                    i = i + 1
                    Do While i <= Len(s) And IsNumeric(Mid$(s, i, 1))
                        buf = buf & Mid$(s, i, 1)
                        i = i + 1
                        If Len(buf) >= 2 Then Exit Do
                    Loop
                    If Len(buf) > 0 Then
                        dd = CLng(buf)
                        If mm >= 1 And mm <= 12 And dd >= 1 And dd <= 31 Then
                            ExtractDate = CStr(mm) & "/" & CStr(dd)
                            Exit Function
                        End If
                    End If
                End If
            End If
        End If
NextI:
    Next i

    ' パターン2: M月D日
    Dim pos As Long, pos2 As Long
    pos = InStr(s, "月")
    If pos > 1 And pos < Len(s) Then
        pos2 = InStr(pos, s, "日")
        If pos2 > pos Then
            Dim ms As String, ds As String
            ms = ExtractLastNumber(Left$(s, pos - 1))
            ds = ExtractFirstNumber(Mid$(s, pos + 1, pos2 - pos - 1))
            If Len(ms) > 0 And Len(ds) > 0 Then
                mm = CLng(ms): dd = CLng(ds)
                If mm >= 1 And mm <= 12 And dd >= 1 And dd <= 31 Then
                    ExtractDate = CStr(mm) & "/" & CStr(dd)
                    Exit Function
                End If
            End If
        End If
    End If

    ExtractDate = ""
End Function

Private Function ExtractLastNumber(ByVal s As String) As String
    Dim i As Long, buf As String, found As Boolean
    For i = Len(s) To 1 Step -1
        If IsNumeric(Mid$(s, i, 1)) Then
            buf = Mid$(s, i, 1) & buf
            found = True
        ElseIf found Then
            Exit For
        End If
    Next i
    ExtractLastNumber = buf
End Function

Private Function ExtractFirstNumber(ByVal s As String) As String
    Dim i As Long, buf As String, found As Boolean
    For i = 1 To Len(s)
        If IsNumeric(Mid$(s, i, 1)) Then
            buf = buf & Mid$(s, i, 1)
            found = True
        ElseIf found Then
            Exit For
        End If
    Next i
    ExtractFirstNumber = buf
End Function

'--- 対象年月生成（yyyy/M 形式） ---
Private Function BuildYearMonth(ByVal baseYear As Long, ByVal md As String) As String
    If Len(md) = 0 Then
        BuildYearMonth = ""
        Exit Function
    End If
    Dim parts() As String
    parts = Split(md, "/")
    If UBound(parts) < 1 Then BuildYearMonth = "": Exit Function
    BuildYearMonth = CStr(baseYear) & "/" & CStr(CLng(parts(0)))
End Function

'--- 部屋番号と診療科を分離 ---
Private Sub SplitRoomAndDept(ByVal s As String, ByRef room As String, ByRef dept As String)
    Dim segs() As String
    Dim src As String
    src = NormalizeSeparators(s)

    ' まず「room」を含む単位を優先抽出
    room = ExtractRoomToken(src)

    ' 診療科抽出
    dept = ExtractDept(src)

    ' 元原文の先頭近くにある「1room・消外・E9」のような区切りブロックがあれば整形
    ' ここでは E9 のような「E列（外来病棟略号）」も部屋番号候補に追加
    Dim eWard As String
    eWard = ExtractEWard(src)
    If Len(eWard) > 0 Then
        If Len(room) = 0 Then
            room = eWard
        Else
            If InStr(room, eWard) = 0 Then room = room & "・" & eWard
        End If
    End If

    ' 「2A」「9room」等の階・部屋番号
    Dim aRoom As String
    aRoom = ExtractANumRoom(src)
    If Len(aRoom) > 0 Then
        If Len(room) = 0 Then
            room = aRoom
        ElseIf InStr(room, aRoom) = 0 Then
            room = room & "・" & aRoom
        End If
    End If
End Sub

'--- 区切り記号を統一（・/／,、） → 「・」 ---
Private Function NormalizeSeparators(ByVal s As String) As String
    Dim t As String
    t = s
    t = Replace(t, "／", "・")
    t = Replace(t, ",", "・")
    t = Replace(t, "、", "・")
    NormalizeSeparators = t
End Function

'--- 「4room」「10room」など「数字+room」抽出 ---
Private Function ExtractRoomToken(ByVal s As String) As String
    Dim i As Long, buf As String, out As String
    Dim ls As String
    ls = LCase$(s)
    i = 1
    Do While i <= Len(ls)
        If IsNumeric(Mid$(ls, i, 1)) Then
            buf = ""
            Do While i <= Len(ls) And IsNumeric(Mid$(ls, i, 1))
                buf = buf & Mid$(ls, i, 1)
                i = i + 1
            Loop
            ' 数字直後が "room" なら採用
            If i + 3 <= Len(ls) Then
                If Mid$(ls, i, 4) = "room" Then
                    If Len(out) > 0 Then out = out & "・"
                    out = out & buf & "room"
                    i = i + 4
                End If
            End If
        Else
            i = i + 1
        End If
    Loop
    ExtractRoomToken = out
End Function

'--- 「2A」「10B」等（数字+アルファベット1文字、心外/心臓外科系病棟）抽出 ---
Private Function ExtractANumRoom(ByVal s As String) As String
    Dim i As Long, buf As String, out As String
    i = 1
    Do While i <= Len(s)
        If IsNumeric(Mid$(s, i, 1)) Then
            buf = ""
            Do While i <= Len(s) And IsNumeric(Mid$(s, i, 1))
                buf = buf & Mid$(s, i, 1)
                i = i + 1
            Loop
            If i <= Len(s) Then
                Dim c As String
                c = UCase$(Mid$(s, i, 1))
                ' 「2A」「10B」など、直後が大文字アルファベット1字で、その次が更に英字ではない
                If c Like "[A-Z]" Then
                    Dim next2 As String
                    If i + 1 <= Len(s) Then next2 = UCase$(Mid$(s, i + 1, 1)) Else next2 = ""
                    ' room の r は除外
                    If UCase$(Mid$(s, i, 4)) <> "ROOM" And Not (next2 Like "[A-Z]") Then
                        ' 病棟表記らしいか（buf の桁数が1〜2、cは A-D 程度）
                        If Len(buf) <= 2 And ("ABCDE" Like "*" & c & "*") Then
                            If Len(out) > 0 Then out = out & "・"
                            out = out & buf & c
                        End If
                        i = i + 1
                    End If
                End If
            End If
        Else
            i = i + 1
        End If
    Loop
    ExtractANumRoom = out
End Function

'--- 「E9」「E7」等（病棟略号）抽出 ---
Private Function ExtractEWard(ByVal s As String) As String
    Dim i As Long, out As String
    For i = 1 To Len(s) - 1
        Dim c1 As String, c2 As String
        c1 = UCase$(Mid$(s, i, 1))
        c2 = Mid$(s, i + 1, 1)
        If (c1 = "E" Or c1 = "W") And IsNumeric(c2) Then
            ' 前が英字でないこと
            If i = 1 Then
                ' OK
            Else
                Dim prev As String
                prev = UCase$(Mid$(s, i - 1, 1))
                If prev Like "[A-Z]" Then GoTo NextE
            End If
            Dim buf As String, j As Long
            buf = c1
            j = i + 1
            Do While j <= Len(s) And IsNumeric(Mid$(s, j, 1))
                buf = buf & Mid$(s, j, 1)
                j = j + 1
                If Len(buf) >= 3 Then Exit Do
            Loop
            If Len(buf) >= 2 Then
                If InStr(out, buf) = 0 Then
                    If Len(out) > 0 Then out = out & "・"
                    out = out & buf
                End If
            End If
        End If
NextE:
    Next i
    ExtractEWard = out
End Function

'--- 診療科抽出（辞書ベース） ---
'   【重要】判定は「長い語」から先にチェック（例：「心臓外科」を「心外」より先に）
Private Function ExtractDept(ByVal s As String) As String
    ' 外科系（消化器）
    If InStr(s, "消化器外科") > 0 Then ExtractDept = "外科（消化器含む）": Exit Function
    If InStr(s, "消化外") > 0 Then ExtractDept = "外科（消化器含む）": Exit Function
    If InStr(s, "消外") > 0 Then ExtractDept = "外科（消化器含む）": Exit Function
    If InStr(s, "消化器") > 0 Then ExtractDept = "外科（消化器含む）": Exit Function
    ' 呼吸器外科
    If InStr(s, "呼吸器外科") > 0 Then ExtractDept = "呼吸器外科": Exit Function
    If InStr(s, "呼外") > 0 Then ExtractDept = "呼吸器外科": Exit Function
    ' 整形外科
    If InStr(s, "整形外科") > 0 Then ExtractDept = "整形外科": Exit Function
    If InStr(s, "整形") > 0 Then ExtractDept = "整形外科": Exit Function
    ' 脳外
    If InStr(s, "脳神経外科") > 0 Then ExtractDept = "脳外": Exit Function
    If InStr(s, "脳外") > 0 Then ExtractDept = "脳外": Exit Function
    ' 心外
    If InStr(s, "心臓血管外科") > 0 Then ExtractDept = "心外": Exit Function
    If InStr(s, "心臓外科") > 0 Then ExtractDept = "心外": Exit Function
    If InStr(s, "心外") > 0 Then ExtractDept = "心外": Exit Function
    ' 産婦（婦人科）
    If InStr(s, "産婦人科") > 0 Then ExtractDept = "産婦（婦人科）": Exit Function
    If InStr(s, "婦人科") > 0 Then ExtractDept = "産婦（婦人科）": Exit Function
    If InStr(s, "産科") > 0 Then ExtractDept = "産婦（婦人科）": Exit Function
    If InStr(s, "産婦") > 0 Then ExtractDept = "産婦（婦人科）": Exit Function
    ' 泌尿器
    If InStr(s, "泌尿器科") > 0 Then ExtractDept = "泌尿器": Exit Function
    If InStr(s, "泌尿器") > 0 Then ExtractDept = "泌尿器": Exit Function
    ' 耳鼻
    If InStr(s, "耳鼻咽喉科") > 0 Then ExtractDept = "耳鼻": Exit Function
    If InStr(s, "耳鼻科") > 0 Then ExtractDept = "耳鼻": Exit Function
    If InStr(s, "耳鼻") > 0 Then ExtractDept = "耳鼻": Exit Function
    ' 口腔外科
    If InStr(s, "口腔外科") > 0 Then ExtractDept = "口腔外科": Exit Function
    If InStr(s, "口外") > 0 Then ExtractDept = "口腔外科": Exit Function
    ' 形成外科
    If InStr(s, "形成外科") > 0 Then ExtractDept = "形成外科": Exit Function
    If InStr(s, "形成") > 0 Then ExtractDept = "形成外科": Exit Function
    ' 眼科・麻酔科・一般外科
    If InStr(s, "眼科") > 0 Then ExtractDept = "眼科": Exit Function
    If InStr(s, "麻酔科") > 0 Then ExtractDept = "麻酔科（機器主管）": Exit Function
    If InStr(s, "外科") > 0 Then ExtractDept = "外科（消化器含む）": Exit Function

    ExtractDept = ""
End Function

'--- 職種推定（麻酔科/CE/NS） ---
Private Function DetectRole(ByVal s As String, ByRef whyOut As String) As String
    ' スコアリング方式：語彙ごとに +1
    Dim scMa As Long, scCe As Long, scNs As Long
    Dim whyMa As String, whyCe As String, whyNs As String

    ' --- 麻酔科キーワード ---
    Dim kwMa As Variant
    kwMa = Split("麻酔科医|麻酔医|全麻|脊麻|硬膜外|ブロック|挿管チューブ|気管挿管|麻酔カート|アドレナリン|ロクロニウム|アセリオ|セフトリアキソン|麻酔同意|SGシース|動脈ライン|術前ライン|GAIA|血圧値|アセト|セフェム|鎮静|自科麻酔|麻酔科オカレンス|麻酔同意書", "|")
    Dim i As Long
    For i = LBound(kwMa) To UBound(kwMa)
        If InStr(s, kwMa(i)) > 0 Then
            scMa = scMa + 1
            If Len(whyMa) < 40 Then whyMa = whyMa & IIf(Len(whyMa) > 0, ",", "") & kwMa(i)
        End If
    Next i

    ' --- CE(臨床工学技士)キーワード ---
    Dim kwCe As Variant
    kwCe = Split("除細動器|体外式PM|ペースメーカ|モニター不良|ME機器|ハーモニック|X-P機器|レントゲン機器|電気メス|エコー機器|内視鏡機器|人工心肺|透析機器|透析装置|SCD本体|SCD装置|アドスプレー噴霧器材|ベリプラスト|噴霧装置|機器不良|機器の不良|装置不良", "|")
    For i = LBound(kwCe) To UBound(kwCe)
        If InStr(s, kwCe(i)) > 0 Then
            scCe = scCe + 1
            If Len(whyCe) < 40 Then whyCe = whyCe & IIf(Len(whyCe) > 0, ",", "") & kwCe(i)
        End If
    Next i

    ' --- NS(看護師)キーワード ---
    Dim kwNs As Variant
    kwNs = Split("SCD|DVT|SCD装着|健側|麻痺側|入室遅れ|入室を呼|帰室|病棟にTEL|病棟へ|洗組|滅菌|ステラッド|器械|介助医|術中針|廃液|排水槽|血液を含む廃液|日勤リーダー|出頭時間|飲水|家族が飲水|HCU|看護|Ns|NS|師長|プロフィール|既往歴|薬剤師|入退室|麻酔同意書を親|同意が取れた|同意書|病棟から持参|病棟に持参|持参するよう伝え|持参忘れ|E7|E9|半身麻痺|右半身麻痺|左半身麻痺|血圧測定|執刀医に確認|病棟Ns", "|")
    For i = LBound(kwNs) To UBound(kwNs)
        If InStr(s, kwNs(i)) > 0 Then
            scNs = scNs + 1
            If Len(whyNs) < 40 Then whyNs = whyNs & IIf(Len(whyNs) > 0, ",", "") & kwNs(i)
        End If
    Next i

    ' 明示ラベルがあれば最優先
    If InStr(s, "職種：麻酔科") > 0 Or InStr(s, "麻酔科オカレンス") > 0 Then
        DetectRole = "麻酔科": whyOut = "明示ラベル:麻酔科"
        Exit Function
    ElseIf InStr(s, "職種：CE") > 0 Or InStr(s, "CEオカレンス") > 0 Then
        DetectRole = "CE": whyOut = "明示ラベル:CE"
        Exit Function
    ElseIf InStr(s, "職種：NS") > 0 Or InStr(s, "NSオカレンス") > 0 Then
        DetectRole = "NS": whyOut = "明示ラベル:NS"
        Exit Function
    End If

    ' 最大スコアを採用
    Dim maxSc As Long
    maxSc = scMa
    If scCe > maxSc Then maxSc = scCe
    If scNs > maxSc Then maxSc = scNs

    If maxSc = 0 Then
        DetectRole = ""
        whyOut = ""
        Exit Function
    End If

    If scMa = maxSc Then
        DetectRole = "麻酔科": whyOut = "麻酔:" & whyMa
    ElseIf scCe = maxSc Then
        DetectRole = "CE": whyOut = "CE:" & whyCe
    ElseIf scNs = maxSc Then
        DetectRole = "NS": whyOut = "NS:" & whyNs
    End If
End Function

'--- 分類推定（確認不足・準備不足/機器/薬剤/コミュ/体制/その他） ---
Private Function DetectCategory(ByVal s As String, ByRef whyOut As String) As String
    Dim scConf As Long, scDev As Long, scDrug As Long, scComm As Long, scOrg As Long
    Dim whyConf As String, whyDev As String, whyDrug As String, whyComm As String, whyOrg As String

    ' 確認不足・準備不足
    Dim kwConf As Variant
    kwConf = Split("持参忘れ|持ち込み忘れ|置き忘れ|忘れ|確認漏れ|既往歴|健側|麻痺側|アレルギー|同意書|同意が取れ|準備不足|補充されていない|補充されておらず|準備も出来|洗組に伝わらず|滅菌されなかった|記録が残ってな|記録されて|セフェム系アレルギー|プロフィールの既往", "|")
    Dim i As Long
    For i = LBound(kwConf) To UBound(kwConf)
        If InStr(s, kwConf(i)) > 0 Then
            scConf = scConf + 1
            If Len(whyConf) < 40 Then whyConf = whyConf & IIf(Len(whyConf) > 0, ",", "") & kwConf(i)
        End If
    Next i

    ' 機器
    Dim kwDev As Variant
    kwDev = Split("機器不良|機器の不良|不良|モニター|除細動器|ペースメーカ|体外式PM|ハーモニック|X-P|レントゲン|電気メス|SCD本体|落下|破損|割れた|動作しない|エラー|アドスプレー|噴霧装置|装置|コード断線|ディスポ|フック部分が割れ|バイタル飛ばず", "|")
    For i = LBound(kwDev) To UBound(kwDev)
        If InStr(s, kwDev(i)) > 0 Then
            scDev = scDev + 1
            If Len(whyDev) < 40 Then whyDev = whyDev & IIf(Len(whyDev) > 0, ",", "") & kwDev(i)
        End If
    Next i

    ' 薬剤
    Dim kwDrug As Variant
    kwDrug = Split("麻薬|薬剤|アセリオ|ソルアセト|ヘパリン|生食|注射用水|セフトリアキソン|セフェム|ロクロニウム|アドレナリン|輸液|点滴|抗菌薬|こぼした|投与忘れ|投与間違い|誤投与", "|")
    For i = LBound(kwDrug) To UBound(kwDrug)
        If InStr(s, kwDrug(i)) > 0 Then
            scDrug = scDrug + 1
            If Len(whyDrug) < 40 Then whyDrug = whyDrug & IIf(Len(whyDrug) > 0, ",", "") & kwDrug(i)
        End If
    Next i

    ' コミュ
    Dim kwComm As Variant
    kwComm = Split("伝え忘れ|伝わらず|情報が伝わ|TEL|連絡|申し送り|呼んでいないが|呼んでいない|師長に情報|出頭時間を伝え|報告なし|共有されず|確認せず|指示がなく", "|")
    For i = LBound(kwComm) To UBound(kwComm)
        If InStr(s, kwComm(i)) > 0 Then
            scComm = scComm + 1
            If Len(whyComm) < 40 Then whyComm = whyComm & IIf(Len(whyComm) > 0, ",", "") & kwComm(i)
        End If
    Next i

    ' 体制
    Dim kwOrg As Variant
    kwOrg = Split("30分待|30分ほど|時間が遅れ|遅れた|OP開始が遅れ|入室遅れ|帰室が|HCUではなく|緊急手術|夜間|時間外|人員不足|スタッフ不足|配置|体制|業務手順|手順が", "|")
    For i = LBound(kwOrg) To UBound(kwOrg)
        If InStr(s, kwOrg(i)) > 0 Then
            scOrg = scOrg + 1
            If Len(whyOrg) < 40 Then whyOrg = whyOrg & IIf(Len(whyOrg) > 0, ",", "") & kwOrg(i)
        End If
    Next i

    ' 最大スコアを採用（同点はこの順で優先： 確認 > 薬剤 > 機器 > コミュ > 体制）
    Dim maxSc As Long
    maxSc = scConf
    If scDrug > maxSc Then maxSc = scDrug
    If scDev > maxSc Then maxSc = scDev
    If scComm > maxSc Then maxSc = scComm
    If scOrg > maxSc Then maxSc = scOrg

    If maxSc = 0 Then
        DetectCategory = "その他"
        whyOut = "該当キーワードなし→その他"
        Exit Function
    End If

    If scConf = maxSc Then
        DetectCategory = "確認不足・準備不足": whyOut = "確認:" & whyConf
    ElseIf scDrug = maxSc Then
        DetectCategory = "薬剤": whyOut = "薬剤:" & whyDrug
    ElseIf scDev = maxSc Then
        DetectCategory = "機器": whyOut = "機器:" & whyDev
    ElseIf scComm = maxSc Then
        DetectCategory = "コミュ": whyOut = "コミュ:" & whyComm
    ElseIf scOrg = maxSc Then
        DetectCategory = "体制": whyOut = "体制:" & whyOrg
    End If
End Function

'--- 時間帯推定 ---
Private Function DetectTimeSlot(ByVal s As String) As String
    If InStr(s, "緊急") > 0 Then DetectTimeSlot = "緊急": Exit Function
    If InStr(s, "夜間") > 0 Or InStr(s, "深夜") > 0 Then DetectTimeSlot = "夜間（19時〜）": Exit Function
    If InStr(s, "時間外") > 0 Then DetectTimeSlot = "夕方（17〜19時）": Exit Function

    ' 「8:50」「17:30」などの時刻から判定
    Dim i As Long, hh As Long
    For i = 1 To Len(s) - 3
        If IsNumeric(Mid$(s, i, 1)) Then
            Dim j As Long, buf As String
            j = i
            Do While j <= Len(s) And IsNumeric(Mid$(s, j, 1))
                buf = buf & Mid$(s, j, 1)
                j = j + 1
                If Len(buf) >= 2 Then Exit Do
            Loop
            If j <= Len(s) And Len(buf) > 0 Then
                Dim sep As String
                sep = Mid$(s, j, 1)
                If sep = ":" Or sep = "：" Then
                    hh = CLng(buf)
                    If hh >= 0 And hh <= 23 Then
                        If hh < 12 Then
                            DetectTimeSlot = "午前（〜12時）"
                        ElseIf hh < 17 Then
                            DetectTimeSlot = "午後（12〜17時）"
                        ElseIf hh < 19 Then
                            DetectTimeSlot = "夕方（17〜19時）"
                        Else
                            DetectTimeSlot = "夜間（19時〜）"
                        End If
                        Exit Function
                    End If
                End If
            End If
        End If
    Next i

    DetectTimeSlot = ""
End Function

'--- 備考テキスト構築 ---
Private Function BuildNote(ByVal roleWhy As String, ByVal catWhy As String) As String
    Dim s As String
    If Len(roleWhy) > 0 Then s = "[職種] " & roleWhy
    If Len(catWhy) > 0 Then
        If Len(s) > 0 Then s = s & " / "
        s = s & "[分類] " & catWhy
    End If
    BuildNote = s
End Function

'=====================================================================
'                    ヘルパー
'=====================================================================
Private Function GetOrCreateSheet(ByVal nm As String) As Worksheet
    Dim ws As Worksheet
    If SheetExists(nm) Then
        Set GetOrCreateSheet = ThisWorkbook.Worksheets(nm)
    Else
        Set ws = ThisWorkbook.Worksheets.Add( After:=ThisWorkbook.Worksheets(ThisWorkbook.Worksheets.Count))
        ws.Name = nm
        Set GetOrCreateSheet = ws
    End If
End Function

Private Function SheetExists(ByVal nm As String) As Boolean
    Dim ws As Worksheet
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets(nm)
    SheetExists = Not ws Is Nothing
    On Error GoTo 0
End Function

Private Function NzNum(ByVal v As Variant, ByVal fallback As Double) As Double
    If IsNumeric(v) Then
        NzNum = CDbl(v)
    Else
        NzNum = fallback
    End If
End Function
