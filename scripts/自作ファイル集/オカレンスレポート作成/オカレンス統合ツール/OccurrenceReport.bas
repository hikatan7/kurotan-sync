Attribute VB_Name = "OccurrenceReport"
Option Explicit

'=====================================================================
'  手術室オカレンス・マンスリーレポート自動生成マクロ v2（オフライン動作）
'  入力：①基本入力 ②月別推移 ③クロス集計 ④時間帯・診療科 ⑤コメント
'  出力：このブックと同じフォルダに Word文書(.docx) を生成
'  必要環境：Excel + Word（同一PC）。ネット接続・追加ライブラリ不要。
'  v2変更点：推移グラフの「合計」系列をG列（合計）から取得するよう修正／
'            ②の「※」注記行を月として拾わないよう修正／既存ファイル上書き対応
'=====================================================================

'--- Word定数（遅延バインディング用） ---
Private Const wdCollapseEnd As Long = 0
Private Const wdAlignParagraphCenter As Long = 1
Private Const wdBorderBottom As Long = -3
Private Const wdLineStyleSingle As Long = 1
Private Const wdFormatXMLDocument As Long = 12

'--- 色 ---
Private mNavy As Long, mLBlue As Long, mGray As Long

'--- Wordオブジェクト（モジュール共有） ---
Private mWd As Object, mDoc As Object

'=====================================================================
Public Sub オカレンスレポート作成()
    Dim wsB As Worksheet, wsT As Worksheet, wsX As Worksheet
    Dim wsJ As Worksheet, wsC As Worksheet
    On Error GoTo EH

    Set wsB = ThisWorkbook.Worksheets("①基本入力")
    Set wsT = ThisWorkbook.Worksheets("②月別推移")
    Set wsX = ThisWorkbook.Worksheets("③クロス集計")
    Set wsJ = ThisWorkbook.Worksheets("④時間帯・診療科")
    Set wsC = ThisWorkbook.Worksheets("⑤コメント")

    ' レポート作成前に当月件数を②月別推移へ自動反映（反映忘れ防止）
    UpsertTrend True

    mNavy = RGB(31, 56, 100): mLBlue = RGB(217, 226, 243): mGray = RGB(85, 85, 85)

    '---------- 基本値の取得 ----------
    Dim yy As String, mm As String
    yy = CStr(wsB.Range("B3").Value): mm = CStr(wsB.Range("B4").Value)

    Dim ops As Double, opsAn As Double, nMa As Double, nCe As Double, nNs As Double
    Dim prevOps As Double, prevTot As Double, tot As Double
    ops = Nz(wsB.Range("B6")): opsAn = Nz(wsB.Range("B7"))
    nMa = Nz(wsB.Range("B9")): nCe = Nz(wsB.Range("B10")): nNs = Nz(wsB.Range("B11"))
    prevOps = Nz(wsB.Range("B13")): prevTot = Nz(wsB.Range("B14"))
    tot = nMa + nCe + nNs

    Dim rate As String, prevRate As String, diffPt As String
    Dim maRate As String, ceRate As String, nsRate As String
    rate = Pct(tot, ops): prevRate = Pct(prevTot, prevOps)
    If rate <> "―" And prevRate <> "―" Then
        diffPt = Format(CDbl(rate) - CDbl(prevRate), "+0.0;-0.0;±0.0") & "pt"
    Else
        diffPt = "―"
    End If
    maRate = Pct(nMa, opsAn): ceRate = Pct(nCe, ops): nsRate = Pct(nNs, ops)

    '---------- Word起動・文書設定 ----------
    Set mWd = CreateObject("Word.Application")
    mWd.Visible = False
    mWd.DisplayAlerts = 0
    Set mDoc = mWd.Documents.Add
    With mDoc.PageSetup
        .TopMargin = mWd.CentimetersToPoints(1.1)
        .BottomMargin = mWd.CentimetersToPoints(1.1)
        .LeftMargin = mWd.CentimetersToPoints(1.4)
        .RightMargin = mWd.CentimetersToPoints(1.4)
    End With
    With mDoc.Styles(-1).Font   ' -1 = wdStyleNormal（標準スタイル）
        .Name = "游ゴシック": .NameFarEast = "游ゴシック": .Size = 10
    End With
    With mDoc.Styles(-1).ParagraphFormat
        .SpaceBefore = 1: .SpaceAfter = 1: .LineSpacingRule = 0
    End With

    '---------- タイトル ----------
    Para "手術室オカレンス・マンスリーレポート（" & yy & "年" & mm & "月度）", 15, True, 0, 0
    Para "集計対象：麻酔科／CE／NS オカレンスレポート（" & yy & "年" & mm & "月分）", 8, False, mGray, 0

    '========== 1. 概況 ==========
    Heading "1. 概況（総括）"
    Dim t As Object
    Set t = NewTable(3, 4, Array(4.2, 4.6, 4.2, 5.2))
    HCell t, 1, 1, "総オカレンス件数": SCell t, 1, 2, Fmt0(tot) & " 件", True, False
    HCell t, 1, 3, "内訳": SCell t, 1, 4, "麻酔科: " & Fmt0(nMa) & ", CE: " & Fmt0(nCe) & ", NS: " & Fmt0(nNs), False, False
    HCell t, 2, 1, "全手術件数"
    SCell t, 2, 2, IIf(ops > 0, Fmt0(ops) & " 件（麻酔科管理 " & Fmt0S(opsAn) & "件）", "― 件"), True, False
    HCell t, 2, 3, "報告率": SCell t, 2, 4, rate & " ％（前月比 " & diffPt & "）", True, False
    HCell t, 3, 1, "100手術あたり発生率": SCell t, 3, 2, rate & " 件（前月 " & prevRate & "件）", True, False
    HCell t, 3, 3, "重大度(Lv3a以上)"
    SCell t, 3, 4, NzS(wsB.Range("B19")) & " 件" & IIf(Trim(wsB.Range("B19").Text) = "", "（未評価）", ""), False, False
    Para "【重大度別件数】 Level 0: " & NzS(wsB.Range("B16")) & "件 / Level 1: " & NzS(wsB.Range("B17")) & _
         "件 / Level 2: " & NzS(wsB.Range("B18")) & "件 / Level 3a以上: " & NzS(wsB.Range("B19")) & "件", 9, False, 0, 0
    Para "【職種別報告率】 麻酔科: " & maRate & "％（÷麻酔科管理" & Fmt0S(opsAn) & "件） / CE: " & ceRate & _
         "％ / NS: " & nsRate & "％（÷総手術" & Fmt0S(ops) & "件）。※報告率＝オカレンス報告件数÷手術件数と定義", 9, False, 0, 0
    If Nz(wsB.Range("B21")) > 0 Then
        Para "【麻酔科の参考値】 総報告数（オカレンスなし含む）: " & Fmt0(Nz(wsB.Range("B21"))) & _
             "件 / うちオカレンスなし: " & Fmt0(Nz(wsB.Range("B22"))) & "件", 9, False, mGray, 0
    End If

    '========== 2. 月別推移 ==========
    Heading "2. 月別推移"
    Dim n As Long, i As Long
    n = 0
    Do While Trim(wsT.Cells(3 + n, 1).Text) <> "" And Left$(Trim(wsT.Cells(3 + n, 1).Text), 1) <> "※" And n < 24
        n = n + 1
    Loop
    If n > 0 Then
        ' 直近3か月の総括表
        Dim s As Long, r As Long, k As Long
        s = IIf(n >= 3, n - 2, 1)
        Set t = NewTable(n - s + 2, 4, Array(2.4, 5#, 4.4, 4.6))
        HCell t, 1, 1, "月": HCell t, 1, 2, "手術件数": HCell t, 1, 3, "オカレンス件数": HCell t, 1, 4, "100手術あたり発生率"
        r = 2
        For i = s To n
            Dim mOps As Double, mTot As Double
            mOps = Nz(wsT.Cells(2 + i, 5))
            mTot = Nz(wsT.Cells(2 + i, 2)) + Nz(wsT.Cells(2 + i, 3)) + Nz(wsT.Cells(2 + i, 4))
            SCell t, r, 1, wsT.Cells(2 + i, 1).Text, False, True
            SCell t, r, 2, IIf(mOps > 0, Fmt0(mOps), "―"), i = n, False
            SCell t, r, 3, Fmt0(mTot), i = n, False
            SCell t, r, 4, Pct(mTot, mOps), i = n, False
            r = r + 1
        Next i

        ' 職種別推移表（左右2分割・10列）
        Para "【職種別オカレンスレポート報告件数の推移】", 9, True, 0, 0
        Dim half As Long
        half = Int((n + 1) / 2)
        Set t = NewTable(half + 1, 10, Array(2#, 1.5, 1.3, 1.3, 1.5, 2#, 1.5, 1.3, 1.3, 1.5))
        For k = 0 To 1
            HCell t, 1, k * 5 + 1, "月": HCell t, 1, k * 5 + 2, "麻酔科": HCell t, 1, k * 5 + 3, "CE"
            HCell t, 1, k * 5 + 4, "NS": HCell t, 1, k * 5 + 5, "合計"
        Next k
        For i = 1 To n
            Dim rr As Long, cc As Long
            If i <= half Then rr = i + 1: cc = 0 Else rr = i - half + 1: cc = 5
            SCell t, rr, cc + 1, wsT.Cells(2 + i, 1).Text, False, True
            SCell t, rr, cc + 2, NzS(wsT.Cells(2 + i, 2)), False, False
            SCell t, rr, cc + 3, NzS(wsT.Cells(2 + i, 3)), False, False
            SCell t, rr, cc + 4, NzS(wsT.Cells(2 + i, 4)), False, False
            SCell t, rr, cc + 5, Fmt0(Nz(wsT.Cells(2 + i, 2)) + Nz(wsT.Cells(2 + i, 3)) + Nz(wsT.Cells(2 + i, 4))), True, False
        Next i

        ' 折れ線グラフ（Excelで作成→画像として貼付）
        PasteTrendChart wsT, n
    End If
    ' 推移コメント
    Dim hasCmt As Boolean
    hasCmt = False
    For i = 3 To 5
        If Trim(wsC.Cells(i, 2).Text) <> "" Then hasCmt = True
    Next i
    If hasCmt Then
        Para "● コメント（推移の解釈）", 10, True, 0, 0
        For i = 3 To 5
            If Trim(wsC.Cells(i, 2).Text) <> "" Then Bullet wsC.Cells(i, 2).Text
        Next i
    End If

    '========== 3. クロス集計 ==========
    Heading "3. 職種別 × 分類別件数（クロス集計）"
    Dim catName(1 To 6) As String, catTot(1 To 6) As Double
    For i = 1 To 6
        catName(i) = wsX.Cells(2, 1 + i).Text
        catTot(i) = Nz(wsX.Cells(3, 1 + i)) + Nz(wsX.Cells(4, 1 + i)) + Nz(wsX.Cells(5, 1 + i))
    Next i
    Set t = NewTable(5, 8, Array(2.2, 3#, 1.9, 1.9, 1.9, 1.9, 1.9, 1.9))
    HCell t, 1, 1, "職種"
    For i = 1 To 6: HCell t, 1, 1 + i, catName(i): Next i
    HCell t, 1, 8, "計"
    Dim gTot As Double
    For r = 1 To 3
        Dim rowSum As Double
        rowSum = 0
        SCell t, r + 1, 1, wsX.Cells(2 + r, 1).Text, False, True
        For i = 1 To 6
            SCell t, r + 1, 1 + i, Fmt0(Nz(wsX.Cells(2 + r, 1 + i))), False, False
            rowSum = rowSum + Nz(wsX.Cells(2 + r, 1 + i))
        Next i
        SCell t, r + 1, 8, Fmt0(rowSum), True, False
        gTot = gTot + rowSum
    Next r
    HCell t, 5, 1, "計"
    For i = 1 To 6: SCell t, 5, 1 + i, Fmt0(catTot(i)), True, False: Next i
    SCell t, 5, 8, Fmt0(gTot), True, False
    Para "※ 件数は延べ（麻酔科は分類別集計値の合計のため、概況の実件数と一致しない場合があります）", 8, False, mGray, 0
    If Trim(wsC.Range("B40").Text) <> "" Then
        Para "【分類の割付根拠】" & wsC.Range("B40").Text, 8, False, mGray, 0
    End If

    '========== 4. 時間帯別・診療科別 ==========
    Heading "4. 時間帯別・診療科別"
    Dim dName() As String, dCnt() As String, nd As Long
    ReDim dName(1 To 20): ReDim dCnt(1 To 20)
    nd = 0
    Do While Trim(wsJ.Cells(3 + nd, 4).Text) <> "" And nd < 20
        nd = nd + 1
        dName(nd) = wsJ.Cells(2 + nd, 4).Text
        dCnt(nd) = NzS(wsJ.Cells(2 + nd, 5))
    Loop
    Dim halfD As Long
    halfD = Int((nd + 1) / 2)
    Dim nRows As Long
    nRows = 1 + Application.WorksheetFunction.Max(5, halfD)
    Set t = NewTable(nRows, 7, Array(3#, 1.5, 0.4, 3.6, 1.4, 3.6, 1.4))
    HCell t, 1, 1, "時間帯": HCell t, 1, 2, "件数"
    HCell t, 1, 4, "診療科": HCell t, 1, 5, "件数": HCell t, 1, 6, "診療科": HCell t, 1, 7, "件数"
    For i = 1 To 5
        SCell t, 1 + i, 1, wsJ.Cells(2 + i, 1).Text, False, True
        SCell t, 1 + i, 2, NzS(wsJ.Cells(2 + i, 2)), False, False
    Next i
    Dim rr2 As Long, cc2 As Long
    For i = 1 To nd
        If i <= halfD Then rr2 = i + 1: cc2 = 4 Else rr2 = i - halfD + 1: cc2 = 6
        SCell t, rr2, cc2, dName(i), False, True
        SCell t, rr2, cc2 + 1, dCnt(i), False, False
    Next i
    ClearGapColumn t, 3, nRows
    If Trim(wsJ.Range("A9").Text) <> "" Then Para wsJ.Range("A9").Text, 8, False, mGray, 0

    '========== 5. 傾向分析 ==========
    Heading "5. 傾向分析（職種 × 場面 × 要因）"
    If Trim(wsC.Range("B7").Text) <> "" Then
        Para "● 多発場面", 10, True, 0, 0
        Para wsC.Range("B7").Text, 10, False, 0, 0
    End If
    If Trim(wsC.Range("B9").Text & wsC.Range("B10").Text & wsC.Range("B11").Text) <> "" Then
        Para "● 職種別動向", 10, True, 0, 0
        If Trim(wsC.Range("B9").Text) <> "" Then Bullet "麻酔科：" & wsC.Range("B9").Text
        If Trim(wsC.Range("B10").Text) <> "" Then Bullet "CE：" & wsC.Range("B10").Text
        If Trim(wsC.Range("B11").Text) <> "" Then Bullet "NS：" & wsC.Range("B11").Text
    End If
    Dim shellLbl As Variant
    shellLbl = Array("L（申し送り・連絡）：", "E（環境：時間的切迫）：", "H（ハード：機器）：", "S（ソフト：手順）：")
    Dim hasShell As Boolean
    For i = 0 To 3
        If Trim(wsC.Cells(13 + i, 2).Text) <> "" Then hasShell = True
    Next i
    If hasShell Then
        Para "● エラー誘発要因（SHELL＋体制・環境）", 10, True, 0, 0
        For i = 0 To 3
            If Trim(wsC.Cells(13 + i, 2).Text) <> "" Then Bullet shellLbl(i) & wsC.Cells(13 + i, 2).Text
        Next i
    End If

    '========== 6. Pareto分析 ==========
    Heading "6. Pareto分析（3職種合算・延べ" & Fmt0(gTot) & "件）"
    Dim idx(1 To 6) As Long, j As Long, tmp As Long
    For i = 1 To 6: idx(i) = i: Next i
    For i = 1 To 5
        For j = i + 1 To 6
            If catTot(idx(j)) > catTot(idx(i)) Then tmp = idx(i): idx(i) = idx(j): idx(j) = tmp
        Next j
    Next i
    Set t = NewTable(7, 3, Array(6#, 2.2, 2.2))
    HCell t, 1, 1, "項目": HCell t, 1, 2, "件数": HCell t, 1, 3, "累積％"
    Dim cum As Double
    For i = 1 To 6
        cum = cum + catTot(idx(i))
        SCell t, 1 + i, 1, catName(idx(i)), False, True
        SCell t, 1 + i, 2, Fmt0(catTot(idx(i))), False, False
        SCell t, 1 + i, 3, Pct(cum, gTot) & "％", False, False
    Next i
    If gTot > 0 Then
        Para "→ 上位2項目（" & catName(idx(1)) & "＋" & catName(idx(2)) & "）で全体の" & _
             Format((catTot(idx(1)) + catTot(idx(2))) / gTot * 100, "0") & "％を占める。対策資源はこの領域に集中投下が合理的。", 9, False, 0, 0
    End If

    '========== 7. 注目事象とGood Job事例 ==========
    Heading "7. 注目事象とGood Job事例"
    Dim hasAny As Boolean
    hasAny = False
    For i = 18 To 23
        If Trim(wsC.Cells(i, 2).Text) <> "" Then hasAny = True
    Next i
    If hasAny Then
        Para "● 注目リスク事象", 10, True, 0, 0
        For i = 18 To 23
            If Trim(wsC.Cells(i, 2).Text) <> "" Then Bullet wsC.Cells(i, 2).Text
        Next i
    End If
    hasAny = False
    For i = 25 To 28
        If Trim(wsC.Cells(i, 2).Text) <> "" Then hasAny = True
    Next i
    If hasAny Then
        Para "● Good Job / Good Catch", 10, True, 0, 0
        For i = 25 To 28
            If Trim(wsC.Cells(i, 2).Text) <> "" Then Bullet wsC.Cells(i, 2).Text
        Next i
    End If
    If Trim(wsC.Range("B30").Text) <> "" Then Para "● Good Catch率：" & wsC.Range("B30").Text, 9, False, 0, 0

    '========== 8. PDCA ==========
    Heading "8. 安全対策のPDCA（ネクストアクション）"
    hasAny = False
    For i = 32 To 34
        If Trim(wsC.Cells(i, 2).Text) <> "" Then hasAny = True
    Next i
    If hasAny Then
        Para "● 今月の重点課題", 10, True, 0, 0
        For i = 32 To 34
            If Trim(wsC.Cells(i, 2).Text) <> "" Then Bullet wsC.Cells(i, 2).Text
        Next i
    End If
    If Trim(wsC.Range("B36").Text) <> "" Then
        Para "● 改善効果（Before → After）", 10, True, 0, 0
        Para wsC.Range("B36").Text, 10, False, 0, 0
    End If

    '========== 付記 ==========
    Dim fuText As String
    fuText = "【付記】算出不能・未記録の項目は「―」と表示。指標の定義：報告率・100手術あたり発生率＝オカレンス報告件数÷手術件数。" & _
             "職種間で同一事象の重複報告を含む場合、事象ベースの実件数は表記より少ない。報告件数の減少は安全性の向上とは限らず、過少報告の可能性も含めて解釈すること。"
    If Trim(wsC.Range("B38").Text) <> "" Then fuText = fuText & " " & wsC.Range("B38").Text
    Para fuText, 8, False, mGray, 0

    '---------- 保存 ----------
    Dim fPath As String
    fPath = ThisWorkbook.Path & Application.PathSeparator & _
            "手術室オカレンス・マンスリーレポート_" & yy & "年" & mm & "月度.docx"
    mDoc.SaveAs2 fPath, wdFormatXMLDocument
    If AutoMode Then
        mDoc.Close False
        mWd.Quit
        Notify "レポートを作成しました：" & fPath
    Else
        mWd.Visible = True
        mWd.Activate
        MsgBox "レポートを作成しました：" & vbCrLf & fPath, vbInformation, "完了"
    End If
    Set mDoc = Nothing: Set mWd = Nothing
    Exit Sub

EH:
    If AutoMode Then
        Notify "エラーが発生しました（" & Err.Number & "）：" & Err.Description
    Else
        MsgBox "エラーが発生しました（" & Err.Number & "）：" & Err.Description, vbExclamation
    End If
    On Error Resume Next
    If Not mWd Is Nothing Then
        If AutoMode Then mWd.Quit Else mWd.Visible = True
    End If
    Set mDoc = Nothing: Set mWd = Nothing
End Sub

'=====================================================================
'  補助関数
'=====================================================================
Private Function Nz(c As Range) As Double
    If IsNumeric(c.Value) And Trim(c.Text) <> "" Then Nz = CDbl(c.Value) Else Nz = 0
End Function

Private Function NzS(c As Range) As String
    If Trim(c.Text) = "" Then NzS = "―" Else NzS = Trim(c.Text)
End Function

Private Function Fmt0(v As Double) As String
    Fmt0 = Format(v, "0")
End Function

Private Function Fmt0S(v As Double) As String
    If v > 0 Then Fmt0S = Format(v, "0") Else Fmt0S = "―"
End Function

Private Function Pct(num As Double, den As Double) As String
    If den > 0 Then Pct = Format(num / den * 100, "0.0") Else Pct = "―"
End Function

Private Function ER() As Object
    Dim r As Object
    Set r = mDoc.Content
    r.Collapse wdCollapseEnd
    Set ER = r
End Function

Private Sub Para(txt As String, sz As Single, bd As Boolean, colr As Long, algn As Long)
    Dim r As Object
    Set r = ER()
    r.Text = txt & vbCr
    With r.Font
        .Size = sz: .Bold = bd
        If colr <> 0 Then .Color = colr Else .Color = 0
    End With
    With r.ParagraphFormat
        .Alignment = algn
        .SpaceBefore = 1: .SpaceAfter = 1
        .Borders(wdBorderBottom).LineStyle = 0   ' 見出し罫線の引き継ぎ防止
    End With
End Sub

Private Sub Bullet(txt As String)
    Dim r As Object
    Set r = ER()
    r.Text = "・" & txt & vbCr
    r.Font.Size = 10: r.Font.Bold = False: r.Font.Color = 0
    With r.ParagraphFormat
        .LeftIndent = mWd.CentimetersToPoints(0.3)
        .SpaceBefore = 1: .SpaceAfter = 1
        .Borders(wdBorderBottom).LineStyle = 0
    End With
End Sub

Private Sub Heading(txt As String)
    Dim r As Object
    Set r = ER()
    r.Text = txt & vbCr
    With r.Font
        .Size = 12: .Bold = True: .Color = mNavy
    End With
    With r.ParagraphFormat
        .SpaceBefore = 8: .SpaceAfter = 3
        With .Borders(wdBorderBottom)
            .LineStyle = wdLineStyleSingle
            .Color = mNavy
        End With
    End With
End Sub

' 表を文書末尾に追加（widthsCm：列幅cm配列）
Private Function NewTable(nr As Long, nc As Long, widthsCm As Variant) As Object
    Dim t As Object, i As Long
    Set t = mDoc.Tables.Add(ER(), nr, nc)
    t.AllowAutoFit = False
    t.Borders.Enable = True
    For i = 1 To nc
        t.Columns(i).SetWidth mWd.CentimetersToPoints(CDbl(widthsCm(i - 1))), 0
    Next i
    t.Range.ParagraphFormat.SpaceBefore = 0
    t.Range.ParagraphFormat.SpaceAfter = 0
    Set NewTable = t
End Function

Private Sub HCell(t As Object, r As Long, c As Long, txt As String)
    With t.Cell(r, c)
        .Range.Text = txt
        .Shading.BackgroundPatternColor = mNavy
        .Range.Font.Color = RGB(255, 255, 255)
        .Range.Font.Bold = True
        .Range.Font.Size = 9
        .Range.ParagraphFormat.Alignment = wdAlignParagraphCenter
    End With
End Sub

Private Sub SCell(t As Object, r As Long, c As Long, txt As String, bd As Boolean, subShade As Boolean)
    With t.Cell(r, c)
        .Range.Text = txt
        .Range.Font.Size = 9
        .Range.Font.Bold = bd
        .Range.Font.Color = 0
        If subShade Then .Shading.BackgroundPatternColor = mLBlue
        .Range.ParagraphFormat.Alignment = wdAlignParagraphCenter
    End With
End Sub

' 区切り列（罫線・網掛けなし）にする
Private Sub ClearGapColumn(t As Object, colIdx As Long, nRows As Long)
    Dim i As Long
    On Error Resume Next
    For i = 1 To nRows
        With t.Cell(i, colIdx)
            .Borders.Enable = False
            .Shading.BackgroundPatternColor = -16777216   ' wdColorAutomatic
            .Range.Text = ""
        End With
    Next i
    On Error GoTo 0
End Sub

' 推移グラフをExcelで作成しWordへ画像貼付
Private Sub PasteTrendChart(wsT As Worksheet, n As Long)
    Dim co As ChartObject, r As Object
    On Error GoTo Skip
    Set co = wsT.ChartObjects.Add(300, 10, 470, 240)
    With co.Chart
        .ChartType = xlLine
        Dim sr As Series
        Set sr = .SeriesCollection.NewSeries
        sr.Name = "麻酔科": sr.XValues = wsT.Range(wsT.Cells(3, 1), wsT.Cells(2 + n, 1))
        sr.Values = wsT.Range(wsT.Cells(3, 2), wsT.Cells(2 + n, 2))
        sr.Format.Line.ForeColor.RGB = RGB(31, 91, 142): sr.Format.Line.Weight = 2.2
        Set sr = .SeriesCollection.NewSeries
        sr.Name = "CE": sr.Values = wsT.Range(wsT.Cells(3, 3), wsT.Cells(2 + n, 3))
        sr.Format.Line.ForeColor.RGB = RGB(224, 123, 57): sr.Format.Line.Weight = 2.2
        Set sr = .SeriesCollection.NewSeries
        sr.Name = "NS": sr.Values = wsT.Range(wsT.Cells(3, 4), wsT.Cells(2 + n, 4))
        sr.Format.Line.ForeColor.RGB = RGB(46, 125, 50): sr.Format.Line.Weight = 2.2
        Set sr = .SeriesCollection.NewSeries
        sr.Name = "合計": sr.Values = wsT.Range(wsT.Cells(3, 7), wsT.Cells(2 + n, 7))
        sr.Format.Line.ForeColor.RGB = RGB(154, 165, 177): sr.Format.Line.Weight = 1.5
        sr.Format.Line.DashStyle = 4   ' msoLineDash
        .HasTitle = True
        .ChartTitle.Text = "オカレンスレポート報告件数の推移"
        .ChartTitle.Font.Size = 11
        .Legend.Position = xlLegendPositionBottom
        .Axes(xlCategory).TickLabels.Font.Size = 8
        .Axes(xlValue).TickLabels.Font.Size = 8
        .Axes(xlValue).MinimumScale = 0
    End With
    co.Chart.CopyPicture Appearance:=xlScreen, Format:=xlPicture
    Set r = ER()
    r.Paste
    r.ParagraphFormat.Alignment = wdAlignParagraphCenter
    Set r = ER()
    r.Text = vbCr
Skip:
    On Error Resume Next
    If Not co Is Nothing Then co.Delete
    On Error GoTo 0
End Sub
