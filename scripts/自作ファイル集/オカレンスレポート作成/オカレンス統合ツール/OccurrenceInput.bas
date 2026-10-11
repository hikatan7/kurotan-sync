Attribute VB_Name = "OccurrenceInput"
Option Explicit

'=====================================================================
'  手術室オカレンス報告 収集・自動振り分けマクロ v2（オフライン動作）
'
'  対応する貼り付け形式（⑦貼付エリアに貼るだけ・自動判定）：
'    A) 麻酔科サマリ  … Word報告の本文（「34.手術準備不足 45件」等の集計行）
'                       → 件数を読み取り J列に記録（延べ件数として集計）
'                       → 「総計」「99.オカレンスなし」は K列（参考件数）へ
'    B) CE表         … 日付|主科|機器|内容 の表（日付は前行から引き継ぎ）
'    C) NS表         … 日|診療科or部屋|出来事 の表
'    D) 1行テキスト   … 従来どおり1行=1報告として解析
'
'  自動処理：対象年月・職種・部屋番号・分類・診療科・時間帯・判定根拠
'  必要環境：Excel（マクロ有効ブック）のみ。ネット接続不要。
'=====================================================================

Private Const PASTE_SHEET As String = "⑦貼付エリア"
Private Const TARGET_SHEET As String = "⑥報告収集"
Private Const BASE_SHEET As String = "①基本入力"
Private Const TREND_SHEET As String = "②月別推移"
Private Const CONF_SHEET As String = "⑨設定"

Private Const CAT_REF_TOTAL As String = "参考（総計）"
Private Const CAT_REF_NONE As String = "参考（オカレンスなし）"

' エラー発生位置の追跡用（転記のエラーメッセージに含める）
Private mProg As String

'=====================================================================
' シート「⑦貼付エリア」を初期化（無ければ作成、あれば内容クリア）
'=====================================================================
Public Sub 貼付エリア初期化()
    Dim ws As Worksheet
    Set ws = GetOrCreateSheet(PASTE_SHEET)

    Application.ScreenUpdating = False
    ws.Cells.Clear

    With ws
        .Range("A1").Value = "▼ A3以降に、麻酔科報告の本文／CE表／NS表 をそのまま貼り付けてください（形式は自動判定）。"
        .Range("A1").Font.Bold = True
        .Range("A1").Interior.Color = RGB(255, 242, 204)
        .Range("A1").Font.Color = RGB(120, 60, 0)

        .Range("C1").Value = "▼オプション"
        .Range("C1").Font.Bold = True
        .Range("D1").Value = "既定の職種："
        .Range("E1").Value = "自動推定"
        .Range("E1").Validation.Delete
        .Range("E1").Validation.Add Type:=xlValidateList, Formula1:="自動推定,麻酔科,CE,NS"

        .Range("F1").Value = "既定の時間帯："
        .Range("G1").Value = ""
        .Range("G1").Validation.Delete
        .Range("G1").Validation.Add Type:=xlValidateList, Formula1:=" ,午前（～12時）,午後（12～17時）,夕方（17～19時）,夜間（19時～）,緊急"

        .Range("H1").Value = "データの年（西暦）："
        .Range("I1").Value = ""
        .Range("I1").Interior.Color = RGB(255, 255, 204)
        .Range("J1").Value = "貼付形式："
        .Range("K1").Value = "自動判定"
        .Range("K1").Validation.Delete
        .Range("K1").Validation.Add Type:=xlValidateList, Formula1:="自動判定,麻酔科サマリ,CE表,NS表,1行テキスト"

        .Range("A2").Value = "（年が空欄なら①基本入力の対象年を使用。貼り付け後 Alt+F8→「報告収集へ転記」、またはシート上のボタンを実行）"
        .Range("A2").Font.Color = RGB(120, 120, 120)
        .Range("A2").Font.Italic = True

        .Columns("A").ColumnWidth = 60
        .Columns("B:D").ColumnWidth = 16
        .Columns("E:K").ColumnWidth = 13
        .Rows(1).RowHeight = 22

        .Activate
        .Range("A3").Select
    End With

    Application.ScreenUpdating = True
    Notify "「" & PASTE_SHEET & "」を準備しました。A3以降に貼り付けてください。"
End Sub

'=====================================================================
' メイン：⑦貼付エリアの内容を解析して ⑥報告収集 の末尾に追記
'=====================================================================
Public Sub 報告収集へ転記()
    Dim wsP As Worksheet, wsT As Worksheet, wsB As Worksheet
    mProg = ""
    On Error GoTo EH

    If Not SheetExists(PASTE_SHEET) Then
        貼付エリア初期化
        Exit Sub
    End If
    Set wsP = ThisWorkbook.Worksheets(PASTE_SHEET)
    Set wsT = ThisWorkbook.Worksheets(TARGET_SHEET)
    Set wsB = ThisWorkbook.Worksheets(BASE_SHEET)

    ' データの年（⑦I1 → 空欄なら①対象年 → それも無ければ今年）
    Dim baseYear As Long
    baseYear = CLng(NzNum(wsP.Range("I1").Value, NzNum(wsB.Range("B3").Value, Year(Date))))
    Dim baseMonth As Long
    baseMonth = CLng(NzNum(wsB.Range("B4").Value, Month(Date)))

    Dim defaultRole As String, defaultTime As String, fmtSel As String
    defaultRole = Trim$(CStr(wsP.Range("E1").Value))
    If defaultRole = "自動推定" Then defaultRole = ""
    defaultTime = Trim$(CStr(wsP.Range("G1").Value))
    fmtSel = Trim$(CStr(wsP.Range("K1").Value))
    If fmtSel = "" Then fmtSel = "自動判定"

    ' 貼付範囲（A～D列の最終行の最大値）
    Dim lastR As Long, c As Long, lr As Long
    lastR = 0
    For c = 1 To 5
        lr = wsP.Cells(wsP.Rows.Count, c).End(xlUp).Row
        If lr > lastR Then lastR = lr
    Next c
    If lastR < 3 Then
        Notify "貼付エリアが空です。A3以降に貼り付けてから実行してください。"
        Exit Sub
    End If

    ' 形式判定
    Dim layout As String
    If fmtSel = "自動判定" Then
        layout = DetectLayout(wsP, lastR)
    Else
        layout = fmtSel
    End If

    ' ⑥報告収集の書き込み開始行
    Dim wrRow As Long
    wrRow = wsT.Cells(wsT.Rows.Count, "D").End(xlUp).Row + 1
    If wrRow < 2 Then wrRow = 2

    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual

    Dim addedCount As Long, skippedCount As Long
    Select Case layout
        Case "CE表"
            ParseCETable wsP, wsT, lastR, wrRow, baseYear, baseMonth, defaultTime, addedCount, skippedCount
        Case "NS表"
            ParseNSTable wsP, wsT, lastR, wrRow, baseYear, baseMonth, defaultTime, addedCount, skippedCount
        Case Else   ' 麻酔科サマリ / 1行テキスト
            ParseTextLines wsP, wsT, lastR, wrRow, baseYear, baseMonth, defaultRole, defaultTime, (layout = "麻酔科サマリ"), addedCount, skippedCount
    End Select

    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    mProg = "転記完了後の後処理"

    Dim msg As String
    msg = "形式「" & layout & "」として " & addedCount & " 行を「" & TARGET_SHEET & "」に追記しました。"
    If skippedCount > 0 Then msg = msg & vbCrLf & "空行・見出し行 " & skippedCount & " 行をスキップしました。"
    msg = msg & vbCrLf & "職種・分類が推定できなかったセルは薄い黄色です。内容を確認してください。"
    Notify msg

    If Not AutoMode Then
        If MsgBox("「" & PASTE_SHEET & "」の貼り付け内容をクリアしますか？", vbYesNo + vbQuestion) = vbYes Then
            ' 行全体を書式ごとクリア（貼り付けで持ち込まれた結合セルがあっても安全）
            wsP.Rows("3:" & Application.WorksheetFunction.Max(lastR + 10, 30)).Clear
            wsP.Activate
            wsP.Range("A3").Select
        End If
    End If
    Exit Sub
EH:
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    Notify "エラーが発生しました：" & Err.Number & " " & Err.Description & IIf(Len(mProg) > 0, "（位置：" & mProg & "）", "")
End Sub

'=====================================================================
' ①基本入力の当月件数を ②月別推移 に反映（行が無ければ追加）
'=====================================================================
Public Sub 当月を月別推移へ反映()
    UpsertTrend False
End Sub

' 本体（silent=True でメッセージなし。Wordレポート作成時に自動実行される）
Public Sub UpsertTrend(ByVal silent As Boolean)
    On Error GoTo EH
    Dim wsB As Worksheet, wsT As Worksheet
    Set wsB = ThisWorkbook.Worksheets(BASE_SHEET)
    Set wsT = ThisWorkbook.Worksheets(TREND_SHEET)

    Dim key As String
    key = MonthKey(wsB)
    If key = "/" Or key = "" Then
        If Not silent Then Notify "①基本入力の対象年・対象月を入力してください。"
        Exit Sub
    End If

    ' 既存行を探す（3～26行、最大24か月）
    Dim r As Long, hitR As Long, blankR As Long
    hitR = 0: blankR = 0
    For r = 3 To 26
        Dim a As String
        a = Trim$(CStr(wsT.Cells(r, 1).Value))
        If a = key Then hitR = r: Exit For
        If a = "" And blankR = 0 Then blankR = r
    Next r
    If hitR = 0 Then
        If blankR = 0 Then
            If Not silent Then Notify "②月別推移が満杯です（最大24か月）。古い行を整理してください。"
            Exit Sub
        End If
        hitR = blankR
        wsT.Cells(hitR, 1).NumberFormat = "@"   ' 「2025/6」が日付に化けるのを防ぐ
        wsT.Cells(hitR, 1).Value = key
    End If

    ' 0件（未取込）の職種は上書きしない
    If NzNum(wsB.Range("B9").Value, 0) > 0 Then wsT.Cells(hitR, 2).Value = wsB.Range("B9").Value
    If NzNum(wsB.Range("B10").Value, 0) > 0 Then wsT.Cells(hitR, 3).Value = wsB.Range("B10").Value
    If NzNum(wsB.Range("B11").Value, 0) > 0 Then wsT.Cells(hitR, 4).Value = wsB.Range("B11").Value
    If NzNum(wsB.Range("B6").Value, 0) > 0 Then wsT.Cells(hitR, 5).Value = wsB.Range("B6").Value
    If NzNum(wsB.Range("B7").Value, 0) > 0 Then wsT.Cells(hitR, 6).Value = wsB.Range("B7").Value
    wsT.Cells(hitR, 7).Formula = "=IF(COUNT(B" & hitR & ":D" & hitR & ")=0,"""",SUM(B" & hitR & ":D" & hitR & "))"

    If Not silent Then Notify key & " の件数を②月別推移の " & hitR & " 行目に反映しました。"
    Exit Sub
EH:
    If Not silent Then Notify "エラーが発生しました：" & Err.Number & " " & Err.Description
End Sub

'=====================================================================
' ⑥報告収集から当月（①の対象年月）の行を削除（やり直し用）
'=====================================================================
Public Sub 当月データを削除()
    On Error GoTo EH
    Dim wsB As Worksheet, wsT As Worksheet
    Set wsB = ThisWorkbook.Worksheets(BASE_SHEET)
    Set wsT = ThisWorkbook.Worksheets(TARGET_SHEET)
    Dim key As String
    key = MonthKey(wsB)

    If Not AutoMode Then
        If MsgBox("⑥報告収集から 対象年月 " & key & " の行をすべて削除します。よろしいですか？", vbYesNo + vbExclamation) <> vbYes Then Exit Sub
    End If

    Application.ScreenUpdating = False
    Dim lastR As Long, r As Long, delCount As Long
    lastR = wsT.Cells(wsT.Rows.Count, "D").End(xlUp).Row
    For r = lastR To 2 Step -1
        If Trim$(CStr(wsT.Cells(r, 2).Value)) = key Then
            wsT.Rows(r).Delete
            delCount = delCount + 1
        End If
    Next r
    Application.ScreenUpdating = True
    Notify key & " の " & delCount & " 行を削除しました。"
    Exit Sub
EH:
    Application.ScreenUpdating = True
    Notify "エラーが発生しました：" & Err.Number & " " & Err.Description
End Sub

'=====================================================================
' ⑤コメントの自動作成（当月の⑥データから件数・割合付きで生成）
'   ・推移コメント（B3:B5）は手入力欄のため触らない
'   ・すでに記入済みの欄は上書きしない（作り直す場合は欄を消して再実行）
'   ・データから判断できない欄は空白のまま
'=====================================================================
Public Sub コメント自動作成()
    On Error GoTo EH
    Dim wsB As Worksheet, wsT As Worksheet, wsC As Worksheet
    Set wsB = ThisWorkbook.Worksheets(BASE_SHEET)
    Set wsT = ThisWorkbook.Worksheets(TARGET_SHEET)
    Set wsC = ThisWorkbook.Worksheets("⑤コメント")

    Dim key As String
    key = MonthKey(wsB)
    If key = "/" Or key = "" Then
        Notify "①基本入力の対象年・対象月を入力してください。"
        Exit Sub
    End If

    '---------- 集計 ----------
    Dim catName(1 To 6) As String
    catName(1) = "確認不足・準備不足": catName(2) = "機器": catName(3) = "薬剤"
    catName(4) = "コミュ": catName(5) = "体制": catName(6) = "その他"
    Dim roleName(1 To 3) As String
    roleName(1) = "麻酔科": roleName(2) = "CE": roleName(3) = "NS"

    Dim catTot(1 To 6) As Double, roleTot(1 To 3) As Double
    Dim catRole(1 To 3, 1 To 6) As Double
    Dim deptN(1 To 60) As String, deptC(1 To 60) As Double, nDept As Long
    Dim timeN(1 To 5) As String, timeC(1 To 5) As Double
    timeN(1) = "午前（～12時）": timeN(2) = "午後（12～17時）": timeN(3) = "夕方（17～19時）"
    timeN(4) = "夜間（19時～）": timeN(5) = "緊急"
    Dim devN(1 To 300) As String, devC(1 To 300) As Double, nDev As Long
    Dim refTotal As Double, refNone As Double

    Dim riskTxt(1 To 6) As String, nRisk As Long
    Dim gjTxt(1 To 4) As String, nGj As Long
    Dim kwRisk As Variant, kwGj As Variant
    kwRisk = Split("大量出血|出血性|ショック|心マ|VF|DC実施|アナフィラキ|取り違え|左右が違う|左右の|誤薬|誤投与|重複投与|破損|骨折|抜管後|SpO2低下|再挿管|誤嚥|転倒|熱傷|針刺し", "|")
    kwGj = Split("気付き|気付いた|気付き是正|気づき|気づいた|未然|防止できた|発見し|臨床使用前に|事前に共有|事前情報|立ち会い|Good", "|")

    Dim lastR As Long, r As Long
    lastR = wsT.Cells(wsT.Rows.Count, "D").End(xlUp).Row
    Dim nData As Long
    For r = 2 To lastR
        If Trim$(CStr(wsT.Cells(r, 2).Value)) <> key Then GoTo NextR
        nData = nData + 1
        Dim roleS As String, catS As String, deptS As String, timeS As String, genS As String
        Dim jv As Double, kv As Double
        roleS = Trim$(CStr(wsT.Cells(r, 3).Value))
        catS = Trim$(CStr(wsT.Cells(r, 6).Value))
        deptS = Trim$(CStr(wsT.Cells(r, 7).Value))
        timeS = Trim$(CStr(wsT.Cells(r, 8).Value))
        genS = CStr(wsT.Cells(r, 4).Value)
        jv = NzNum(wsT.Cells(r, 10).Value, 0)
        kv = NzNum(wsT.Cells(r, 11).Value, 0)

        If catS = CAT_REF_TOTAL Then refTotal = refTotal + kv: GoTo Harvest
        If catS = CAT_REF_NONE Then refNone = refNone + kv: GoTo Harvest

        Dim ci As Long, ri As Long, i As Long
        ci = 0: ri = 0
        For i = 1 To 6
            If catS = catName(i) Then ci = i
        Next i
        For i = 1 To 3
            If roleS = roleName(i) Then ri = i
        Next i
        If ci > 0 Then catTot(ci) = catTot(ci) + jv
        If ri > 0 Then roleTot(ri) = roleTot(ri) + jv
        If ci > 0 And ri > 0 Then catRole(ri, ci) = catRole(ri, ci) + jv

        If jv > 0 And deptS <> "" Then
            Dim f As Long
            f = 0
            For i = 1 To nDept
                If deptN(i) = deptS Then f = i
            Next i
            If f = 0 And nDept < 60 Then nDept = nDept + 1: deptN(nDept) = deptS: f = nDept
            If f > 0 Then deptC(f) = deptC(f) + jv
        End If
        If jv > 0 And timeS <> "" Then
            For i = 1 To 5
                If timeS = timeN(i) Then timeC(i) = timeC(i) + jv
            Next i
        End If
        ' CE原文の【機器名】を頻度集計
        If InStr(genS, "【") > 0 And InStr(genS, "】") > InStr(genS, "【") Then
            Dim dv As String
            dv = Mid$(genS, InStr(genS, "【") + 1, InStr(genS, "】") - InStr(genS, "【") - 1)
            If Len(dv) > 0 And Len(dv) <= 20 Then
                f = 0
                For i = 1 To nDev
                    If devN(i) = dv Then f = i
                Next i
                If f = 0 And nDev < 300 Then nDev = nDev + 1: devN(nDev) = dv: f = nDev
                If f > 0 Then devC(f) = devC(f) + 1
            End If
        End If

Harvest:
        ' 注目リスク事象・Good Job候補（明細行含む全行から抽出）
        If nRisk < 6 Then
            For i = LBound(kwRisk) To UBound(kwRisk)
                If InStr(genS, kwRisk(i)) > 0 Then
                    nRisk = nRisk + 1
                    riskTxt(nRisk) = "（自動抽出）" & Trunc70(genS)
                    Exit For
                End If
            Next i
        End If
        If nGj < 4 Then
            For i = LBound(kwGj) To UBound(kwGj)
                If InStr(genS, kwGj(i)) > 0 Then
                    nGj = nGj + 1
                    gjTxt(nGj) = "（自動抽出）" & Trunc70(genS)
                    Exit For
                End If
            Next i
        End If
NextR:
    Next r

    If nData = 0 Then
        Notify "⑥報告収集に対象年月 " & key & " のデータがありません。先にレポートを取り込んでください。"
        Exit Sub
    End If

    Dim tot As Double
    Dim i2 As Long
    For i2 = 1 To 6
        tot = tot + catTot(i2)
    Next i2

    '---------- 上位の特定 ----------
    Dim top1 As Long, top2 As Long
    top1 = MaxIdx6(catTot, 0)
    top2 = MaxIdx6(catTot, top1)
    Dim topDept As Long, topTime As Long
    topDept = 0
    For i2 = 1 To nDept
        If topDept = 0 Then
            topDept = i2
        ElseIf deptC(i2) > deptC(topDept) Then
            topDept = i2
        End If
    Next i2
    topTime = 0
    For i2 = 1 To 5
        If topTime = 0 Then
            topTime = i2
        ElseIf timeC(i2) > timeC(topTime) Then
            topTime = i2
        End If
    Next i2

    Dim filled As Long

    '---------- B7 多発場面 ----------
    If tot > 0 Then
        Dim s7 As String
        s7 = "当月は「" & catName(top1) & "」が延べ" & Fmt0(catTot(top1)) & "件（" & Pct1(catTot(top1), tot) & "％）で最多"
        If top2 > 0 Then
            If catTot(top2) > 0 Then s7 = s7 & "、次いで「" & catName(top2) & "」" & Fmt0(catTot(top2)) & "件（" & Pct1(catTot(top2), tot) & "％）"
        End If
        s7 = s7 & "。"
        If topDept > 0 Then
            If deptC(topDept) > 0 Then s7 = s7 & "診療科別では" & deptN(topDept) & "（" & Fmt0(deptC(topDept)) & "件）"
        End If
        If topTime > 0 Then
            If timeC(topTime) > 0 Then s7 = s7 & "、時間帯では" & timeN(topTime) & "（" & Fmt0(timeC(topTime)) & "件）に比較的集中。"
        End If
        FillIfEmpty wsC, "B7", s7, filled
    End If

    '---------- B9:B11 職種別動向 ----------
    Dim ri2 As Long
    For ri2 = 1 To 3
        If roleTot(ri2) > 0 Then
            Dim tc As Long, sR As String
            Dim tmpArr(1 To 6) As Double
            For i2 = 1 To 6
                tmpArr(i2) = catRole(ri2, i2)
            Next i2
            tc = MaxIdx6(tmpArr, 0)
            If tc > 0 Then
                sR = "延べ" & Fmt0(roleTot(ri2)) & "件。最多は「" & catName(tc) & "」" & Fmt0(catRole(ri2, tc)) & "件（" & Pct1(catRole(ri2, tc), roleTot(ri2)) & "％）。"
            Else
                sR = "延べ" & Fmt0(roleTot(ri2)) & "件。"
            End If
            If ri2 = 1 And refTotal > 0 Then
                sR = "総報告" & Fmt0(refTotal) & "件、うちオカレンスなし" & Fmt0(refNone) & "件（" & Pct1(refNone, refTotal) & "％）・実オカレンス" & Fmt0(refTotal - refNone) & "件。" & sR
            End If
            FillIfEmpty wsC, "B" & (8 + ri2), sR, filled
        End If
    Next ri2

    '---------- B13:B16 SHELL ----------
    If catTot(4) > 0 Then FillIfEmpty wsC, "B13", "コミュニケーション関連は延べ" & Fmt0(catTot(4)) & "件（" & Pct1(catTot(4), tot) & "％）。申し送り・連絡経路の確認が必要。", filled
    Dim eCnt As Double
    eCnt = timeC(5) + timeC(4)
    If eCnt > 0 Then FillIfEmpty wsC, "B14", "緊急" & Fmt0(timeC(5)) & "件・夜間" & Fmt0(timeC(4)) & "件。時間的切迫下での発生に注意。", filled
    If catTot(2) > 0 Then
        Dim sH As String
        sH = "機器関連は延べ" & Fmt0(catTot(2)) & "件（" & Pct1(catTot(2), tot) & "％）。"
        Dim d1 As Long
        d1 = 0
        For i2 = 1 To nDev
            If d1 = 0 Then
                d1 = i2
            ElseIf devC(i2) > devC(d1) Then
                d1 = i2
            End If
        Next i2
        If d1 > 0 Then
            If devC(d1) >= 2 Then sH = sH & "頻出機器：" & devN(d1) & "（" & Fmt0(devC(d1)) & "件）。"
        End If
        FillIfEmpty wsC, "B15", sH, filled
    End If
    If catTot(1) > 0 Then FillIfEmpty wsC, "B16", "確認不足・準備不足は延べ" & Fmt0(catTot(1)) & "件（" & Pct1(catTot(1), tot) & "％）。チェックリスト・準備手順の網羅性を点検。", filled

    '---------- B18:B23 注目リスク事象 ----------
    For i2 = 1 To nRisk
        FillIfEmpty wsC, "B" & (17 + i2), riskTxt(i2), filled
    Next i2

    '---------- B25:B28 Good Job ----------
    For i2 = 1 To nGj
        FillIfEmpty wsC, "B" & (24 + i2), gjTxt(i2), filled
    Next i2

    '---------- B32:B33 重点課題 ----------
    If tot > 0 Then
        FillIfEmpty wsC, "B32", "（自動案）最多分類「" & catName(top1) & "」（" & Fmt0(catTot(top1)) & "件・" & Pct1(catTot(top1), tot) & "％）への対策を最優先（該当手順・チェックリストの見直し）。", filled
        If top2 > 0 Then
            If catTot(top2) > 0 Then FillIfEmpty wsC, "B33", "（自動案）第2位「" & catName(top2) & "」（" & Fmt0(catTot(top2)) & "件・" & Pct1(catTot(top2), tot) & "％）の再発パターンを検証。", filled
        End If
    End If

    '---------- B40 割付根拠 ----------
    FillIfEmpty wsC, "B40", "分類はキーワード辞書による自動割付（各行の根拠は⑥報告収集の備考欄）。麻酔科は報告書の分類番号→大分類対応表（⑨設定）で割付。", filled

    wsC.Activate
    Notify filled & " 個の欄を自動作成しました（記入済みの欄と、データから判断できない欄はそのまま）。" & vbCrLf & _
           "「（自動抽出）（自動案）」の行は内容を確認・編集してください。推移コメント（B3:B5）は手入力欄です。"
    Exit Sub
EH:
    Notify "エラーが発生しました：" & Err.Number & " " & Err.Description
End Sub

' 空欄のときだけ書き込む
Private Sub FillIfEmpty(ws As Worksheet, ByVal addr As String, ByVal txt As String, ByRef filled As Long)
    If Trim$(CStr(ws.Range(addr).Value)) = "" Then
        ws.Range(addr).Value = txt
        filled = filled + 1
    End If
End Sub

' 6要素配列の最大インデックス（excludeIdx を除外。全て0なら0）
Private Function MaxIdx6(arr() As Double, ByVal excludeIdx As Long) As Long
    Dim i As Long, best As Long
    best = 0
    For i = 1 To 6
        If i <> excludeIdx Then
            If best = 0 Then
                If arr(i) > 0 Then best = i
            ElseIf arr(i) > arr(best) Then
                best = i
            End If
        End If
    Next i
    MaxIdx6 = best
End Function

Private Function Trunc70(ByVal s As String) As String
    Dim t As String
    t = Replace(Replace(Trim$(s), vbCr, " "), vbLf, " ")
    If Len(t) > 70 Then t = Left$(t, 70) & "…"
    Trunc70 = t
End Function

Private Function Fmt0(ByVal v As Double) As String
    Fmt0 = Format(v, "0")
End Function

Private Function Pct1(ByVal num As Double, ByVal den As Double) As String
    If den > 0 Then Pct1 = Format(num / den * 100, "0.0") Else Pct1 = "0.0"
End Function

'=====================================================================
'                    形式判定
'=====================================================================
Private Function DetectLayout(ws As Worksheet, ByVal lastR As Long) As String
    Dim r As Long
    Dim nColC As Long, nColD As Long, nRows As Long
    Dim sumHit As Long
    For r = 3 To lastR
        Dim a As String, b As String, c As String, d As String
        a = Trim$(CStr(ws.Cells(r, 1).Value))
        b = Trim$(CStr(ws.Cells(r, 2).Value))
        c = Trim$(CStr(ws.Cells(r, 3).Value))
        d = Trim$(CStr(ws.Cells(r, 4).Value))
        If a = "" And b = "" And c = "" And d = "" Then GoTo NextR
        nRows = nRows + 1
        ' ヘッダ行で即決
        If a = "日付" And (d = "内容" Or c = "機器") Then DetectLayout = "CE表": Exit Function
        If (a = "日" Or a = "日付") And (c = "出来事" Or InStr(b, "診療科") > 0) Then DetectLayout = "NS表": Exit Function
        If Len(d) > 15 Then nColD = nColD + 1
        If Len(c) > 15 Then nColC = nColC + 1
        Dim dmy As Long, dmy2 As String
        If IsSummaryLine(NormalizeText(a), dmy, dmy2) Then sumHit = sumHit + 1
NextR:
    Next r
    If nRows = 0 Then DetectLayout = "1行テキスト": Exit Function
    If nColD * 2 >= nRows Then DetectLayout = "CE表": Exit Function
    If nColC * 2 >= nRows Then DetectLayout = "NS表": Exit Function
    If sumHit >= 2 Then DetectLayout = "麻酔科サマリ": Exit Function
    DetectLayout = "1行テキスト"
End Function

'=====================================================================
'                    A) 麻酔科サマリ / D) 1行テキスト
'=====================================================================
Private Sub ParseTextLines(wsP As Worksheet, wsT As Worksheet, ByVal lastR As Long, _
                           ByRef wrRow As Long, ByVal baseYear As Long, ByVal baseMonth As Long, _
                           ByVal defaultRole As String, ByVal defaultTime As String, _
                           ByVal forceMasui As Boolean, ByRef addedCount As Long, ByRef skippedCount As Long)
    Dim r As Long
    Dim lastCat As String, lastCatNo As String
    Dim inSummaryCtx As Boolean
    lastCat = ""
    inSummaryCtx = forceMasui

    For r = 3 To lastR
        mProg = "テキスト解析 " & (r - 2) & "行目"
        Dim rawA As String, rawB As String, mergedText As String
        rawA = CStr(wsP.Cells(r, 1).Value)
        rawB = CStr(wsP.Cells(r, 2).Value)
        mergedText = Trim$(rawA)
        If Len(Trim$(rawB)) > 0 Then mergedText = mergedText & " " & Trim$(rawB)

        Dim norm As String
        norm = NormalizeText(mergedText)

        If Len(Trim$(norm)) < 3 Then skippedCount = skippedCount + 1: GoTo NextRow
        If IsHeaderLine(norm) Then
            ' タイトル「オカレンスレポート報告 6月分」から月を取得
            Dim titleMonth As Long
            titleMonth = MonthFromTitle(norm)
            If titleMonth >= 1 And titleMonth <= 12 Then baseMonth = titleMonth
            skippedCount = skippedCount + 1
            GoTo NextRow
        End If

        Dim ym As String
        ym = CStr(baseYear) & "/" & CStr(baseMonth)

        ' --- 総計行（「総計 379件 99.オカレンスなし 283件」の複合行にも対応） ---
        Dim refCnt As Long
        If TryParseTotal(norm, refCnt) Then
            WriteRow wsT, wrRow, ym, "麻酔科", mergedText, "", CAT_REF_TOTAL, "", "", "[麻酔科集計] 総報告数（オカレンスなし含む）", 0, refCnt
            addedCount = addedCount + 1
            ' 同じ行に「99. オカレンスなし 283件」が続く複合行に対応
            Dim cntN As Long, posN As Long, dmyN As Long
            posN = InStr(norm, "オカレンスなし")
            If posN > 0 Then
                cntN = NumBeforeKen(norm, posN, dmyN)
                If cntN > 0 Then
                    WriteRow wsT, wrRow, ym, "麻酔科", "（同上行より）オカレンスなし " & cntN & "件", "", CAT_REF_NONE, "", "", "[麻酔科集計] オカレンスなし件数", 0, cntN
                    addedCount = addedCount + 1
                End If
            End If
            inSummaryCtx = True
            GoTo NextRow
        End If

        ' --- 集計行「N. カテゴリ X件」 ---
        Dim cnt As Long, label As String
        If IsSummaryLine(norm, cnt, label) Then
            Dim catNo As String, mapped As String
            catNo = SummaryCatNo(norm)
            mapped = MapCatNo(catNo)
            If mapped = "対象外" Or InStr(label, "オカレンスなし") > 0 Then
                WriteRow wsT, wrRow, ym, "麻酔科", mergedText, "", CAT_REF_NONE, "", "", "[麻酔科集計] オカレンスなし件数", 0, cnt
            Else
                Dim catWhy As String
                If mapped = "" Then mapped = DetectCategory(label, catWhy)
                WriteRow wsT, wrRow, ym, "麻酔科", mergedText, "", mapped, "", "", "[麻酔科集計] No." & catNo & " " & label & "＝" & cnt & "件", cnt, 0
                lastCat = mapped: lastCatNo = catNo
            End If
            inSummaryCtx = True
            addedCount = addedCount + 1
            GoTo NextRow
        End If

        ' --- 明細行：サマリ文脈では全行を件数0の参考行として記録 ---
        If inSummaryCtx Then
            Dim dCat As String, dWhy As String
            If lastCat <> "" Then
                dCat = lastCat
                dWhy = "[明細] No." & lastCatNo & " の内訳（件数は集計行で計上済み）"
            Else
                dCat = DetectCategory(norm, dWhy)
                dWhy = "[明細] " & dWhy
            End If
            WriteRow wsT, wrRow, ym, "麻酔科", mergedText, "", dCat, "", "", dWhy, 0, 0
            addedCount = addedCount + 1
            GoTo NextRow
        End If

        ' --- 通常の1行=1報告 ---
        Dim md As String, ymL As String
        md = ExtractDate(norm)
        ymL = BuildYearMonth(baseYear, md)
        If ymL = "" Then ymL = ym

        Dim roomStr As String, deptStr As String
        SplitRoomAndDept norm, roomStr, deptStr

        Dim roleStr As String, roleWhy As String
        If forceMasui Then
            roleStr = "麻酔科": roleWhy = "麻酔科サマリ形式"
        Else
            roleStr = DetectRole(norm, roleWhy)
            If roleStr = "" Then roleStr = defaultRole
        End If

        Dim catStr As String, cWhy As String
        catStr = DetectCategory(norm, cWhy)

        Dim timeStr As String
        timeStr = DetectTimeSlot(norm)
        If timeStr = "" Then timeStr = defaultTime

        WriteRow wsT, wrRow, ymL, roleStr, mergedText, roomStr, catStr, deptStr, timeStr, BuildNote(roleWhy, cWhy), 1, 0
        addedCount = addedCount + 1
NextRow:
    Next r
End Sub

'=====================================================================
'                    B) CE表（日付|主科|機器|内容）
'=====================================================================
Private Sub ParseCETable(wsP As Worksheet, wsT As Worksheet, ByVal lastR As Long, _
                         ByRef wrRow As Long, ByVal baseYear As Long, ByVal baseMonth As Long, _
                         ByVal defaultTime As String, ByRef addedCount As Long, ByRef skippedCount As Long)
    Dim r As Long
    Dim curMD As String
    curMD = ""
    For r = 3 To lastR
        mProg = "CE表解析 " & (r - 2) & "行目"
        Dim a As String, b As String, dev As String, cont As String
        a = Trim$(CStr(wsP.Cells(r, 1).Value))
        b = Trim$(CStr(wsP.Cells(r, 2).Value))
        dev = Trim$(CStr(wsP.Cells(r, 3).Value))
        cont = Trim$(CStr(wsP.Cells(r, 4).Value))

        If a = "日付" Or cont = "内容" Then skippedCount = skippedCount + 1: GoTo NextRow
        If cont = "" And dev = "" Then skippedCount = skippedCount + 1: GoTo NextRow

        ' 日付（空欄は前行から引き継ぎ）
        Dim md As String
        md = CellDate(wsP.Cells(r, 1))
        If md <> "" Then curMD = md

        Dim ym As String
        ym = BuildYearMonth(baseYear, curMD)
        If ym = "" Then ym = CStr(baseYear) & "/" & CStr(baseMonth)

        Dim norm As String
        norm = NormalizeText(cont)

        ' 診療科（主科列→本文の順）
        Dim deptStr As String
        deptStr = ExtractDept(NormalizeText(b))
        If deptStr = "" Then deptStr = ExtractDept(norm)

        ' 部屋番号
        Dim roomStr As String, dmy As String
        SplitRoomAndDept norm, roomStr, dmy

        ' 分類（既定＝機器。キーワードで別分類が明確な場合のみ変更）
        Dim catStr As String, cWhy As String
        catStr = DetectCategory(norm & " " & dev, cWhy)
        If catStr = "その他" Then catStr = "機器": cWhy = "CE表の既定分類"

        Dim timeStr As String
        timeStr = DetectTimeSlot(norm)
        If timeStr = "" Then timeStr = defaultTime

        Dim noteStr As String
        noteStr = "[CE表] 機器：" & dev & IIf(Len(cWhy) > 0, " / [分類] " & cWhy, "")

        Dim gen As String
        gen = cont
        If dev <> "" Then gen = "【" & dev & "】" & cont
        If curMD <> "" Then gen = curMD & " " & gen

        WriteRow wsT, wrRow, ym, "CE", gen, roomStr, catStr, deptStr, timeStr, noteStr, 1, 0
        addedCount = addedCount + 1
NextRow:
    Next r
End Sub

'=====================================================================
'                    C) NS表（日|診療科or部屋|出来事）
'=====================================================================
Private Sub ParseNSTable(wsP As Worksheet, wsT As Worksheet, ByVal lastR As Long, _
                         ByRef wrRow As Long, ByVal baseYear As Long, ByVal baseMonth As Long, _
                         ByVal defaultTime As String, ByRef addedCount As Long, ByRef skippedCount As Long)
    Dim r As Long
    Dim curMD As String, prevB As String
    curMD = "": prevB = ""
    For r = 3 To lastR
        mProg = "NS表解析 " & (r - 2) & "行目"
        Dim a As String, b As String, cont As String
        a = Trim$(CStr(wsP.Cells(r, 1).Value))
        b = Trim$(CStr(wsP.Cells(r, 2).Value))
        cont = Trim$(CStr(wsP.Cells(r, 3).Value))

        If a = "日" Or a = "日付" Or cont = "出来事" Then skippedCount = skippedCount + 1: GoTo NextRow
        If cont = "" Then skippedCount = skippedCount + 1: GoTo NextRow

        Dim md As String
        md = CellDate(wsP.Cells(r, 1))
        If md <> "" Then curMD = md

        Dim ym As String
        ym = BuildYearMonth(baseYear, curMD)
        If ym = "" Then ym = CStr(baseYear) & "/" & CStr(baseMonth)

        ' 「同上」は前行の診療科・部屋を引き継ぎ
        If InStr(b, "同上") > 0 Then b = prevB
        If b <> "" Then prevB = b

        Dim norm As String
        norm = NormalizeText(b & "　" & cont)

        Dim roomStr As String, deptStr As String
        SplitRoomAndDept norm, roomStr, deptStr

        Dim catStr As String, cWhy As String
        catStr = DetectCategory(NormalizeText(cont), cWhy)

        Dim timeStr As String
        timeStr = DetectTimeSlot(NormalizeText(cont))
        If timeStr = "" Then timeStr = defaultTime

        Dim gen As String
        gen = cont
        If b <> "" Then gen = "〔" & b & "〕" & cont
        If curMD <> "" Then gen = curMD & " " & gen

        WriteRow wsT, wrRow, ym, "NS", gen, roomStr, catStr, deptStr, timeStr, "[NS表]" & IIf(Len(cWhy) > 0, " [分類] " & cWhy, ""), 1, 0
        addedCount = addedCount + 1
NextRow:
    Next r
End Sub

'=====================================================================
'                    ⑥への行書き込み
'=====================================================================
Private Sub WriteRow(wsT As Worksheet, ByRef wrRow As Long, ByVal ym As String, _
                     ByVal roleStr As String, ByVal gen As String, ByVal roomStr As String, _
                     ByVal catStr As String, ByVal deptStr As String, ByVal timeStr As String, _
                     ByVal noteStr As String, ByVal kensu As Long, ByVal sanko As Long)
    wsT.Cells(wrRow, 1).Formula = "=IF(D" & wrRow & "<>"""",ROW()-1,"""")"
    wsT.Cells(wrRow, 2).NumberFormat = "@"   ' 「2025/6」が日付に化けるのを防ぐ
    wsT.Cells(wrRow, 2).Value = ym
    wsT.Cells(wrRow, 3).Value = roleStr
    wsT.Cells(wrRow, 4).Value = gen
    wsT.Cells(wrRow, 5).Value = roomStr
    wsT.Cells(wrRow, 6).Value = catStr
    wsT.Cells(wrRow, 7).Value = deptStr
    wsT.Cells(wrRow, 8).Value = timeStr
    wsT.Cells(wrRow, 9).Value = noteStr
    wsT.Cells(wrRow, 10).Value = kensu
    If sanko > 0 Then wsT.Cells(wrRow, 11).Value = sanko
    If Len(roleStr) = 0 Then wsT.Cells(wrRow, 3).Interior.Color = RGB(255, 255, 204)
    If Len(catStr) = 0 Then wsT.Cells(wrRow, 6).Interior.Color = RGB(255, 255, 204)
    wrRow = wrRow + 1
End Sub

'=====================================================================
'                    麻酔科サマリ解析
'=====================================================================
' 全角数字・記号を半角へ、全角スペースを半角スペースへ
Private Function NormalizeText(ByVal s As String) As String
    Dim t As String
    t = s
    t = Replace(t, "０", "0"): t = Replace(t, "１", "1"): t = Replace(t, "２", "2")
    t = Replace(t, "３", "3"): t = Replace(t, "４", "4"): t = Replace(t, "５", "5")
    t = Replace(t, "６", "6"): t = Replace(t, "７", "7"): t = Replace(t, "８", "8")
    t = Replace(t, "９", "9")
    t = Replace(t, "　", " ")
    t = Replace(t, "／", "/")
    t = Replace(t, "％", "%")
    NormalizeText = t
End Function

' 「件」の直前にある数値を fromPos 以降から探す（見つからなければ0）
Private Function NumBeforeKen(ByVal s As String, ByVal fromPos As Long, ByRef numStart As Long) As Long
    Dim i As Long, j As Long, buf As String
    If fromPos < 1 Then fromPos = 1
    i = InStr(fromPos, s, "件")
    Do While i > 0
        j = i - 1
        buf = ""
        Do While j >= 1
            If IsNumeric(Mid$(s, j, 1)) Then
                buf = Mid$(s, j, 1) & buf
                j = j - 1
            Else
                Exit Do
            End If
        Loop
        If Len(buf) > 0 And Len(buf) <= 5 Then
            numStart = j + 1
            NumBeforeKen = CLng(buf)
            Exit Function
        End If
        i = InStr(i + 1, s, "件")
    Loop
    NumBeforeKen = 0
    numStart = 0
End Function

' 行頭の数値（最大3桁）を返す。数値の後の位置を nextPos に返す
Private Function LeadingNumber(ByVal s As String, ByRef nextPos As Long) As String
    Dim t As String, i As Long, buf As String
    t = s
    i = 1
    Do While i <= Len(t) And Mid$(t, i, 1) = " "
        i = i + 1
    Loop
    buf = ""
    Do While i <= Len(t) And IsNumeric(Mid$(t, i, 1)) And Len(buf) < 4
        buf = buf & Mid$(t, i, 1)
        i = i + 1
    Loop
    nextPos = i
    LeadingNumber = buf
End Function

' 「N．カテゴリ名　X件」形式か（cnt・labelを返す）
Private Function IsSummaryLine(ByVal norm As String, ByRef cnt As Long, ByRef label As String) As Boolean
    IsSummaryLine = False
    Dim numStr As String, p As Long
    numStr = LeadingNumber(norm, p)
    If numStr = "" Or Len(numStr) > 3 Then Exit Function
    If p > Len(norm) Then Exit Function
    ' 番号の直後は区切り（．.、)
    Dim sep As String
    sep = Mid$(norm, p, 1)
    If sep <> "．" And sep <> "." And sep <> "、" Then Exit Function
    ' 区切り以降で「数値＋件」を探す
    Dim numStart As Long
    cnt = NumBeforeKen(norm, p + 1, numStart)
    If cnt = 0 And numStart = 0 Then Exit Function
    label = Trim$(Mid$(norm, p + 1, numStart - (p + 1)))
    IsSummaryLine = True
End Function

' 集計行の分類番号を返す
Private Function SummaryCatNo(ByVal norm As String) As String
    Dim p As Long
    SummaryCatNo = LeadingNumber(norm, p)
End Function

' 「総計　X件」形式か（行頭が「総計」の行のみ）
Private Function TryParseTotal(ByVal norm As String, ByRef cnt As Long) As Boolean
    TryParseTotal = False
    If Left$(LTrim$(norm), 2) <> "総計" Then Exit Function
    Dim numStart As Long
    cnt = NumBeforeKen(norm, 1, numStart)
    If cnt > 0 Then TryParseTotal = True
End Function

' タイトル「オカレンスレポート報告 6月分」から月を取得（無ければ0）
Private Function MonthFromTitle(ByVal norm As String) As Long
    Dim p As Long, j As Long, buf As String
    MonthFromTitle = 0
    p = InStr(norm, "月分")
    If p <= 1 Then Exit Function
    j = p - 1
    buf = ""
    Do While j >= 1 And Len(buf) < 2
        If IsNumeric(Mid$(norm, j, 1)) Then
            buf = Mid$(norm, j, 1) & buf
            j = j - 1
        Else
            Exit Do
        End If
    Loop
    If Len(buf) > 0 Then MonthFromTitle = CLng(buf)
End Function

' ⑨設定の分類番号マッピング表を引く（見つからなければ ""）
Private Function MapCatNo(ByVal catNo As String) As String
    MapCatNo = ""
    If catNo = "" Then Exit Function
    If Not SheetExists(CONF_SHEET) Then Exit Function
    Dim ws As Worksheet, r As Long
    Set ws = ThisWorkbook.Worksheets(CONF_SHEET)
    For r = 3 To 60
        Dim v As String
        v = Trim$(CStr(ws.Cells(r, 1).Value))
        If v = "" Then Exit For
        If v = catNo Or Val(v) = Val(catNo) Then
            MapCatNo = Trim$(CStr(ws.Cells(r, 3).Value))
            Exit Function
        End If
    Next r
End Function

'=====================================================================
'                    共通ユーティリティ
'=====================================================================
' 対象年月キー（例 2025/6）
Private Function MonthKey(wsB As Worksheet) As String
    MonthKey = Trim$(CStr(wsB.Range("B3").Value)) & "/" & Trim$(CStr(wsB.Range("B4").Value))
End Function

' セルから「M/D」を取り出す（日付型・「4/1（火）」「6月2日（月）」いずれも対応）
Private Function CellDate(c As Range) As String
    Dim v As Variant
    v = c.Value
    If IsDate(v) Then
        CellDate = CStr(Month(v)) & "/" & CStr(Day(v))
        Exit Function
    End If
    CellDate = ExtractDate(NormalizeText(CStr(v)))
End Function

'--- 見出し・区切り行判定 ---
Private Function IsHeaderLine(ByVal s As String) As Boolean
    Dim t As String
    t = Trim$(s)
    If Len(t) = 0 Then IsHeaderLine = True: Exit Function
    If t = "No." Or t = "報告内容" Or t = "報告内容（原文）" Then IsHeaderLine = True: Exit Function
    If InStr(t, "オカレンスレポート報告") > 0 And Len(t) < 30 Then IsHeaderLine = True: Exit Function
    If InStr(t, "以下、") > 0 And InStr(t, "レポート") > 0 Then IsHeaderLine = True: Exit Function
    If t = "その他、重要なもの" Then IsHeaderLine = True: Exit Function
    If Left$(t, 1) = "※" And Len(t) < 60 Then IsHeaderLine = True: Exit Function
    If Len(Replace(Replace(Replace(t, "-", ""), "=", ""), " ", "")) = 0 Then IsHeaderLine = True: Exit Function
    IsHeaderLine = False
End Function

'--- 日付抽出（M/D or M月D日） ---
Private Function ExtractDate(ByVal s As String) As String
    Dim i As Long, ch As String, buf As String
    Dim mm As Long, dd As Long

    ' パターン1: M/D
    For i = 1 To Len(s) - 2
        ch = Mid$(s, i, 1)
        If IsNumeric(ch) Then
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
    If UBound(parts) < 0 Then BuildYearMonth = "": Exit Function
    BuildYearMonth = CStr(baseYear) & "/" & CStr(CLng(parts(0)))
End Function

'--- 部屋番号と診療科を分離 ---
Private Sub SplitRoomAndDept(ByVal s As String, ByRef room As String, ByRef dept As String)
    Dim src As String
    src = NormalizeSeparators(s)

    room = ExtractRoomToken(src)
    dept = ExtractDept(src)

    Dim eWard As String
    eWard = ExtractEWard(src)
    If Len(eWard) > 0 Then
        If Len(room) = 0 Then
            room = eWard
        ElseIf InStr(room, eWard) = 0 Then
            room = room & "・" & eWard
        End If
    End If

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
            If i + 3 <= Len(ls) + 1 Then
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

'--- 「2A」「10B」等抽出 ---
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
                If c Like "[A-Z]" Then
                    Dim next2 As String
                    If i + 1 <= Len(s) Then next2 = UCase$(Mid$(s, i + 1, 1)) Else next2 = ""
                    If UCase$(Mid$(s, i, 4)) <> "ROOM" And Not (next2 Like "[A-Z]") Then
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

'--- 「E9」「W4」等（病棟略号）抽出 ---
Private Function ExtractEWard(ByVal s As String) As String
    Dim i As Long, out As String
    For i = 1 To Len(s) - 1
        Dim c1 As String, c2 As String
        c1 = UCase$(Mid$(s, i, 1))
        c2 = Mid$(s, i + 1, 1)
        If (c1 = "E" Or c1 = "W") And IsNumeric(c2) Then
            If i > 1 Then
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

'--- 診療科抽出（辞書ベース・長い語から先に判定） ---
Private Function ExtractDept(ByVal s As String) As String
    If InStr(s, "消化器外科") > 0 Then ExtractDept = "外科（消化器含む）": Exit Function
    If InStr(s, "消化外") > 0 Then ExtractDept = "外科（消化器含む）": Exit Function
    If InStr(s, "消外") > 0 Then ExtractDept = "外科（消化器含む）": Exit Function
    If InStr(s, "消化器") > 0 Then ExtractDept = "外科（消化器含む）": Exit Function
    If InStr(s, "呼吸器外科") > 0 Then ExtractDept = "呼吸器外科": Exit Function
    If InStr(s, "呼外") > 0 Then ExtractDept = "呼吸器外科": Exit Function
    If InStr(s, "整形外科") > 0 Then ExtractDept = "整形外科": Exit Function
    If InStr(s, "整形") > 0 Then ExtractDept = "整形外科": Exit Function
    If InStr(s, "脳神経外科") > 0 Then ExtractDept = "脳外": Exit Function
    If InStr(s, "脳外") > 0 Then ExtractDept = "脳外": Exit Function
    If InStr(s, "心臓血管外科") > 0 Then ExtractDept = "心外": Exit Function
    If InStr(s, "心臓外科") > 0 Then ExtractDept = "心外": Exit Function
    If InStr(s, "心外") > 0 Then ExtractDept = "心外": Exit Function
    If InStr(s, "産婦人科") > 0 Then ExtractDept = "産婦（婦人科）": Exit Function
    If InStr(s, "婦人科") > 0 Then ExtractDept = "産婦（婦人科）": Exit Function
    If InStr(s, "産科") > 0 Then ExtractDept = "産婦（婦人科）": Exit Function
    If InStr(s, "産婦") > 0 Then ExtractDept = "産婦（婦人科）": Exit Function
    If InStr(s, "泌尿器科") > 0 Then ExtractDept = "泌尿器": Exit Function
    If InStr(s, "泌尿器") > 0 Then ExtractDept = "泌尿器": Exit Function
    If InStr(s, "ウロ") > 0 Then ExtractDept = "泌尿器": Exit Function
    If InStr(s, "耳鼻咽喉科") > 0 Then ExtractDept = "耳鼻": Exit Function
    If InStr(s, "耳鼻科") > 0 Then ExtractDept = "耳鼻": Exit Function
    If InStr(s, "耳鼻") > 0 Then ExtractDept = "耳鼻": Exit Function
    If InStr(s, "口腔外科") > 0 Then ExtractDept = "口腔外科": Exit Function
    If InStr(s, "口外") > 0 Then ExtractDept = "口腔外科": Exit Function
    If InStr(s, "口腔") > 0 Then ExtractDept = "口腔外科": Exit Function
    If InStr(s, "形成外科") > 0 Then ExtractDept = "形成外科": Exit Function
    If InStr(s, "形成") > 0 Then ExtractDept = "形成外科": Exit Function
    If InStr(s, "眼科") > 0 Then ExtractDept = "眼科": Exit Function
    If InStr(s, "麻酔科") > 0 Then ExtractDept = "麻酔科（機器主管）": Exit Function
    If InStr(s, "外科") > 0 Then ExtractDept = "外科（消化器含む）": Exit Function
    ExtractDept = ""
End Function

'--- 職種推定（麻酔科/CE/NS） ---
Private Function DetectRole(ByVal s As String, ByRef whyOut As String) As String
    Dim scMa As Long, scCe As Long, scNs As Long
    Dim whyMa As String, whyCe As String, whyNs As String

    Dim kwMa As Variant
    kwMa = Split("麻酔科医|麻酔医|全麻|脊麻|硬膜外|ブロック|挿管チューブ|気管挿管|麻酔カート|アドレナリン|ロクロニウム|アセリオ|セフトリアキソン|麻酔同意|SGシース|動脈ライン|術前ライン|血圧値|鎮静|自科麻酔|麻酔科オカレンス|麻酔同意書", "|")
    Dim i As Long
    For i = LBound(kwMa) To UBound(kwMa)
        If InStr(s, kwMa(i)) > 0 Then
            scMa = scMa + 1
            If Len(whyMa) < 40 Then whyMa = whyMa & IIf(Len(whyMa) > 0, ",", "") & kwMa(i)
        End If
    Next i

    Dim kwCe As Variant
    kwCe = Split("除細動器|体外式PM|ペースメーカ|モニター不良|ME機器|ハーモニック|X-P機器|レントゲン機器|電気メス|エコー機器|内視鏡機器|人工心肺|透析機器|透析装置|SCD本体|SCD装置|噴霧装置|機器不良|機器の不良|装置不良|始業点検|CEデスク", "|")
    For i = LBound(kwCe) To UBound(kwCe)
        If InStr(s, kwCe(i)) > 0 Then
            scCe = scCe + 1
            If Len(whyCe) < 40 Then whyCe = whyCe & IIf(Len(whyCe) > 0, ",", "") & kwCe(i)
        End If
    Next i

    Dim kwNs As Variant
    kwNs = Split("SCD|DVT|SCD装着|健側|麻痺側|入室遅れ|入室を呼|帰室|病棟にTEL|病棟へ|洗組|滅菌|ステラッド|器械|介助医|術中針|廃液|排水槽|日勤リーダー|出頭時間|飲水|HCU|看護|Ns|NS|師長|プロフィール|既往歴|入退室|同意書|病棟から持参|病棟に持参|持参するよう|持参忘れ|E7|E9|半身麻痺|血圧測定|執刀医に確認|病棟Ns|円座|カウント", "|")
    For i = LBound(kwNs) To UBound(kwNs)
        If InStr(s, kwNs(i)) > 0 Then
            scNs = scNs + 1
            If Len(whyNs) < 40 Then whyNs = whyNs & IIf(Len(whyNs) > 0, ",", "") & kwNs(i)
        End If
    Next i

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

'--- 分類推定 ---
Private Function DetectCategory(ByVal s As String, ByRef whyOut As String) As String
    Dim scConf As Long, scDev As Long, scDrug As Long, scComm As Long, scOrg As Long
    Dim whyConf As String, whyDev As String, whyDrug As String, whyComm As String, whyOrg As String
    Dim i As Long

    Dim kwConf As Variant
    kwConf = Split("持参忘れ|持ち込み忘れ|置き忘れ|外し忘れ|忘れ|確認漏れ|記入漏れ|既往歴|健側|麻痺側|アレルギー|同意書|同意が取れ|準備不足|準備ができて|補充されていない|補充されておらず|洗組に伝わらず|滅菌されなかった|記録が残ってな|不足して|不足し|用意されて|左右|残されていた|置き去り|捨てられて|行方不明|見つからず|カウント", "|")
    For i = LBound(kwConf) To UBound(kwConf)
        If InStr(s, kwConf(i)) > 0 Then
            scConf = scConf + 1
            If Len(whyConf) < 40 Then whyConf = whyConf & IIf(Len(whyConf) > 0, ",", "") & kwConf(i)
        End If
    Next i

    Dim kwDev As Variant
    kwDev = Split("機器不良|機器の不良|不良|モニター|モニタ|除細動器|ペースメーカ|体外式PM|ハーモニック|X-P|レントゲン|電気メス|SCD本体|落下|破損|割れた|動作しない|動作不良|エラー|噴霧装置|装置|コード断線|断線|ディスポ|フリーズ|再起動|映像|ケーブル|接続不良|リークテスト|麻酔器|表示されない|映らない|立ち上がらない|作動して", "|")
    For i = LBound(kwDev) To UBound(kwDev)
        If InStr(s, kwDev(i)) > 0 Then
            scDev = scDev + 1
            If Len(whyDev) < 40 Then whyDev = whyDev & IIf(Len(whyDev) > 0, ",", "") & kwDev(i)
        End If
    Next i

    Dim kwDrug As Variant
    kwDrug = Split("麻薬|薬剤|薬品|アセリオ|ソルアセト|ヘパリン|生食|注射用水|セフトリアキソン|セフェム|ロクロニウム|アドレナリン|エフェドリン|ケタラール|キシロカイン|輸液|点滴|抗菌薬|こぼした|投与忘れ|投与間違い|誤投与|混注|処方", "|")
    For i = LBound(kwDrug) To UBound(kwDrug)
        If InStr(s, kwDrug(i)) > 0 Then
            scDrug = scDrug + 1
            If Len(whyDrug) < 40 Then whyDrug = whyDrug & IIf(Len(whyDrug) > 0, ",", "") & kwDrug(i)
        End If
    Next i

    Dim kwComm As Variant
    kwComm = Split("伝え忘れ|伝わらず|伝えられなかった|情報が伝わ|TEL|連絡|申し送り|呼んでいない|呼んでない|師長に情報|出頭時間を伝え|報告なし|共有されず|確認せず|指示がなく|勘違い|聞き取れ|問い合わせ", "|")
    For i = LBound(kwComm) To UBound(kwComm)
        If InStr(s, kwComm(i)) > 0 Then
            scComm = scComm + 1
            If Len(whyComm) < 40 Then whyComm = whyComm & IIf(Len(whyComm) > 0, ",", "") & kwComm(i)
        End If
    Next i

    Dim kwOrg As Variant
    kwOrg = Split("30分待|30分ほど|時間が遅れ|遅れた|OP開始が遅れ|入室遅れ|帰室が|HCUではなく|緊急手術|夜間|時間外|人員不足|スタッフ不足|配置|体制|業務手順|手順が|時間の延長|延長|待った|遅れる", "|")
    For i = LBound(kwOrg) To UBound(kwOrg)
        If InStr(s, kwOrg(i)) > 0 Then
            scOrg = scOrg + 1
            If Len(whyOrg) < 40 Then whyOrg = whyOrg & IIf(Len(whyOrg) > 0, ",", "") & kwOrg(i)
        End If
    Next i

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
    If InStr(s, "夜間") > 0 Or InStr(s, "深夜") > 0 Then DetectTimeSlot = "夜間（19時～）": Exit Function
    If InStr(s, "時間外") > 0 Then DetectTimeSlot = "夕方（17～19時）": Exit Function

    Dim i As Long, hh As Long
    For i = 1 To Len(s) - 1
        If IsNumeric(Mid$(s, i, 1)) Then
            If i > 1 Then
                If IsNumeric(Mid$(s, i - 1, 1)) Then GoTo NextI
            End If
            Dim j As Long, buf As String
            j = i: buf = ""
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
                            DetectTimeSlot = "午前（～12時）"
                        ElseIf hh < 17 Then
                            DetectTimeSlot = "午後（12～17時）"
                        ElseIf hh < 19 Then
                            DetectTimeSlot = "夕方（17～19時）"
                        Else
                            DetectTimeSlot = "夜間（19時～）"
                        End If
                        Exit Function
                    End If
                End If
            End If
        End If
NextI:
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
        Set ws = ThisWorkbook.Worksheets.Add(After:=ThisWorkbook.Worksheets(ThisWorkbook.Worksheets.Count))
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
    If IsNumeric(v) And Trim$(CStr(v)) <> "" Then
        NzNum = CDbl(v)
    Else
        NzNum = fallback
    End If
End Function

' 自動実行モード（テスト用）：名前定義 OCC_AUTOMODE があれば True
Public Function AutoMode() As Boolean
    Dim nm As Object
    On Error Resume Next
    Set nm = ThisWorkbook.Names("OCC_AUTOMODE")
    AutoMode = Not nm Is Nothing
    On Error GoTo 0
End Function

' メッセージ表示（自動実行モードでは⑨設定のJ2セルに記録）
Public Sub Notify(ByVal msg As String)
    If AutoMode Then
        On Error Resume Next
        ThisWorkbook.Worksheets(CONF_SHEET).Range("J2").Value = msg
        On Error GoTo 0
    Else
        MsgBox msg, vbInformation, "オカレンス統合ツール"
    End If
End Sub
