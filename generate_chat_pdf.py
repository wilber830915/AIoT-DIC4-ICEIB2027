#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成聊天內容總結 PDF"""

from fpdf import FPDF

# 使用系統中文字體
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_PATH_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

class ChatPDF(FPDF):
    def header(self):
        self.set_font("STHeiti", "", 12)
        self.cell(0, 10, "OpenCode 與 Overleaf 整合作業總結", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(5)

    def chapter_title(self, num, title):
        self.set_font("STHeiti", "", 16)
        self.set_fill_color(230, 230, 250)
        self.cell(0, 12, f"{num}. {title}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(4)

    def section_title(self, title):
        self.set_font("STHeiti", "", 13)
        self.set_text_color(50, 50, 150)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def body_text(self, text, size=10):
        self.set_font("STHeiti", "", size)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def code_block(self, text, size=8):
        self.set_font("STHeiti", "", size)
        self.set_fill_color(245, 245, 245)
        self.multi_cell(0, 5, text, fill=True)
        self.ln(2)

    def bullet(self, text, size=10):
        self.set_font("STHeiti", "", size)
        self.cell(8, 6, "\u2022", new_x="RIGHT", new_y="TOP")
        self.multi_cell(0, 6, text)
        self.ln(1)


# 註冊中文字體
pdf = ChatPDF()
pdf.add_font("STHeiti", "", FONT_PATH)
pdf.add_font("STHeiti", "B", FONT_PATH_BOLD)

pdf.add_page()
pdf.set_font("STHeiti", "", 10)

# ==================== 標題頁 ====================
pdf.ln(30)
pdf.set_font("STHeiti", "", 20)
pdf.cell(0, 20, "OpenCode 與 Overleaf 整合作業總結", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(10)
pdf.set_font("STHeiti", "", 12)
pdf.cell(0, 10, "主題 1：OpenCode 連接 Overleaf 與 Overleaf MCP Server 的方法與過程", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.cell(0, 10, "主題 2：使用 OpenCode 串接 Overleaf 編寫內容並同步到 Git 的過程", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(20)
pdf.set_font("STHeiti", "", 10)
pdf.cell(0, 10, "建立日期：2026 年 11 月 25 日", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 10, "GitHub Repo: https://github.com/wilber830915/AIoT-DIC4-ICEIB2027.git", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 10, "Overleaf Project ID: 6b06bb69668f4d5869443455 (AIoT-DIC4)", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 10, "作者: WEN WEI CHENG (wilber830915@gmail.com)", new_x="LMARGIN", new_y="NEXT")

# ==================== 主題 1 ====================
pdf.add_page()
pdf.chapter_title(1, "OpenCode 連接 Overleaf 與 Overleaf MCP Server 的方法與過程")

pdf.section_title("1.1 背景與動機")
pdf.body_text(
    "原本嘗試透過 Git 遠端直接連接 Overleaf（https://git.overleaf.com/6b06bb69668f4d5869443455），"
    "使用 olp_ 開頭的 Git authentication token 進行推送，但 Overleaf 伺服器持續回應："
    "\"This Overleaf project currently has no git access\"，表示該專案的 Git 整合功能尚未啟用。"
    "由於 Overleaf 的 Git 整合通常僅限付費/機構版方案，且需要在網頁介面中個別開啟 Git 存取權限，"
    "因此改為使用 olcli（Overleaf CLI）進行整合。"
)

pdf.section_title("1.2 環境準備")
pdf.code_block(
    "# 安裝 nvm\n"
    "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash\n"
    "\n"
    "# 安裝 Node.js LTS\n"
    "export NVM_DIR=\"$HOME/.nvm\"\n"
    "[ -s \"$NVM_DIR/nvm.sh\" ] && \\. \"$NVM_DIR/nvm.sh\"\n"
    "nvm install --lts   # 安裝 Node.js v26.13.1\n"
    "\n"
    "# 安裝 @aloth/olcli (支援 pull/push/sync/compile + Git remote helper + MCP server)\n"
    "npm install -g @aloth/olcli   # 安裝 olcli v0.18.1\n"
    "olcli --version               # 確認版本\n"
)

pdf.section_title("1.3 認證登入 Overleaf")
pdf.body_text(
    "olcli 的認證需要 Overleaf 的 session cookie（overleaf_session2），而非 Git token。"
    "嘗試使用 olcli auth --browser 開啟瀏覽器登入，但瀏覽器在登入前關閉導致失敗。"
    "最終改用 session cookie 認證："
)
pdf.code_block(
    "# 設定 session cookie 環境變數\n"
    "export OVERLEAF_SESSION=\"s%3ABEy0uj6eTAQzbhqetAWdwziSOjXkZyek.GF70pIxeG0gNjesOd8mrDBnhuWmPLC7bnCsTKjNgsmY\"\n"
    "\n"
    "# 驗證登入狀態\n"
    "olcli auth status\n"
    "# 顯示：Account: wilber830915@gmail.com, Session: valid, 1 project(s)\n"
)
pdf.body_text(
    "認證成功後，帳號為 wilber830915@gmail.com，偵測到 1 個專案。"
)

pdf.section_title("1.4 連接 Overleaf 專案")
pdf.body_text(
    "專案 ID：6b06bb69668f4d5869443455（專案名稱：AIoT-DIC4）"
)
pdf.code_block(
    "# 查看專案詳情\n"
    "olcli info 6b06bb69668f4d5869443455\n"
    "\n"
    "# 下載專案檔案到本地\n"
    "olcli pull 6b06bb69668f4d5869443455 ./overleaf_sync\n"
    "\n"
    "# 上傳本地修改到 Overleaf\n"
    "olcli push --project 6b06bb69668f4d5869443455 .\n"
    "\n"
    "# 雙向同步\n"
    "olcli sync 6b06bb69668f4d5869443455 ./local_dir\n"
    "\n"
    "# 遠端編譯 PDF\n"
    "olcli compile -r main.tex 6b06bb69668f4d5869443455\n"
    "\n"
    "# 編譯並下載 PDF\n"
    "olcli pdf -r main.tex -o output.pdf 6b06bb69668f4d5869443455\n"
)

pdf.section_title("1.5 Overleaf MCP Server 設定")
pdf.body_text(
    "@aloth/olcli 內建 MCP 伺服器 olcli-mcp，可讓 AI 助手透過 MCP 協議與 Overleaf 專案互動。"
    "每個會修改專案的工具（push、delete、rename、comment 等）都會先顯示將要執行的操作，"
    "並等待使用者在客戶端中確認後才寫入，具有安全機制。"
)
pdf.body_text("MCP 伺服器配置（加入 OpenCode ~/.opencode/mcp.json 或對應設定檔）：")
pdf.code_block(
    "{\n"
    '  "mcpServers": {\n'
    '    "overleaf": {\n'
    '      "command": "/Users/wilber/.nvm/versions/node/v26.13.1/bin/olcli-mcp",\n'
    '      "args": [],\n'
    '      "env": {\n'
    '        "OVERLEAF_SESSION": "s%3ABEy0uj6eTAQzbhqetAWdwziSOjXkZyek.GF70pIxeG0gNjesOd8mrDBnhuWmPLC7bnCsTKjNgsmY",\n'
    '        "OVERLEAF_BASE_URL": "https://www.overleaf.com"\n'
    '      }\n'
    '    }\n'
    '  }\n'
    "}\n"
)
pdf.body_text(
    "MCP 支援的工具包括：overleaf_list、overleaf_info、overleaf_pull、overleaf_push、"
    "overleaf_sync、overleaf_diff、overleaf_compile、overleaf_pdf、overleaf_upload、"
    "overleaf_download、overleaf_comments、overleaf_changes 等。"
)

# ==================== 主題 2 ====================
pdf.add_page()
pdf.chapter_title(2, "使用 OpenCode 串接 Overleaf 編寫內容並同步到 Git 的過程")

pdf.section_title("2.1 GitHub 連線與初始化")
pdf.body_text(
    "在本地資料夾 L11_DIC4 中初始化 Git 儲存庫，並連接到 GitHub 遠端："
)
pdf.code_block(
    "git init -b main .\n"
    "git remote add origin git@github.com:wilber830915/AIoT-DIC4-ICEIB2027.git\n"
    "git add -A\n"
    "git commit -m \"Initial commit: ICEIB IEEE Overleaf template\"\n"
    "git push -u origin main\n"
)
pdf.body_text(
    "由於 HTTPS 無法讀取憑證，改用 SSH 遠端（git@github.com:...），"
    "並利用 ~/.ssh/id_ed25519 與 GitHub 進行驗證。"
)

pdf.section_title("2.2 myRef 資料夾併入主 repo")
pdf.body_text(
    "myRef 資料夾原本是獨立的 Git 儲存庫（含自己的 .git 目錄），需要將其併入主 repo："
)
pdf.code_block(
    "rm -rf myRef/.git          # 刪除巢狀 .git\n"
    "git add myRef/\n"
    "git commit -m \"加入 myRef 資料夾（移除其原本的 .git，併入主 repo）\"\n"
    "git push origin main\n"
)

pdf.section_title("2.3 產生 .tex 檔案（300字專業摘要套用 A2Z Outline 格式）")
pdf.body_text(
    "從 300字專業摘要.docx 讀取摘要內容（使用 python-docx），參考 A2Z outline example.pdf 的 A-Z 大綱結構，"
    "將內容映射到 A2Z Outline 的六個章節：Abstract (A-F)、Introduction (G-L)、Related Work (M-O)、"
    "Proposed Scheme (PA-PM)、Simulation (Q-V)、Conclusion (W-Z)，產出 LaTeX 檔案："
)
pdf.code_block(
    "myRef/300字專業摘要_A2Z_Outline.tex\n"
)
pdf.body_text(
    "該檔案使用 article 類別 + xeCJK 中文支援，內容包含："
)
pdf.bullet("Abstract：A (動機)、B (挑戰)、C (解藥)、D (方法設計)、E (實驗)、F (結果)")
pdf.bullet("Introduction：G (現況)、H (挑戰)、I (文獻)、J (評論)、K (設計精神)、L (文章結構)")
pdf.bullet("Related Work：M (方法分類)、N (新趨勢)、O (歸納比較表)")
pdf.bullet("Proposed Scheme：PA-PM (目標、背景、解法、架構、元件、功能、架構圖、達成方式、實作、範例、貢獻、模擬、數學證明)")
pdf.bullet("Simulation：Q-V (實驗量、比較方法、設置、參數調整、結果、驗證)")
pdf.bullet("Conclusion：W-Z (回顧、專精情境、產出、結論與未來工作)")
pdf.bullet("附錄：A2Z 大綱對應總覽表")

pdf.section_title("2.4 擴充 .tex 至約 5 頁")
pdf.body_text(
    "初版 .tex 約 1-2 頁，為達到約 5 頁要求，進行了以下擴充："
)
pdf.bullet("擴充每個 A2Z 小節的詳細說明段落")
pdf.bullet("加入既有方法與 TrailGuard TW 的比較表格 (4x5 歸納表)")
pdf.bullet("加入 TikZ 系統架構圖（五大組件互動流程）")
pdf.bullet("加入數學公式（旅行時間估算、時效性驗證、硬性安全約束、FSR、CSR、MAPE）")
pdf.bullet("加入演算法框（Algorithm 1: TrailGuard TW 風險評估）")
pdf.bullet("加入承諾聲明與作者簡介章節")
pdf.bullet("加入系統參數一覽表")
pdf.bullet("調整行距至 2.0 倍、邊界至 2.0cm、附錄前插入強制分頁")

pdf.section_title("2.5 與 Overleaf 雙向同步")
pdf.body_text(
    "使用 olcli 將本地檔案推送到 Overleaf，並遠端編譯確認頁數："
)
pdf.code_block(
    "# 推送所有檔案到 Overleaf\n"
    "olcli push --project 6b06bb69668f4d5869443455 .\n"
    "\n"
    "# 遠端編譯 PDF\n"
    "olcli compile -r myRef/300字專業摘要_A2Z_Outline.tex 6b06bb69668f4d5869443455\n"
    "\n"
    "# 下載編譯後的 PDF\n"
    "olcli pdf -r myRef/300字專業摘要_A2Z_Outline.tex -o 300字專業摘要_A2Z_Outline.pdf 6b06bb69668f4d5869443455\n"
)
pdf.body_text(
    "注意：Overleaf 編譯器對 xeCJK 中文字體有相容性問題，編譯時建議在 Overleaf 網頁介面中"
    "將 Compiler 切換為 XeLaTeX，方可正確顯示中文內容。"
)

pdf.section_title("2.6 同步到 Git")
pdf.body_text(
    "所有本地修改皆透過 Git commit 並推送到 GitHub，確保版本控制："
)
pdf.code_block(
    "git add -A\n"
    "git commit -m \"更新說明\"\n"
    "git push origin main\n"
)
pdf.body_text(
    "Git 提交紀錄摘要："
)
pdf.code_block(
    "257e039 Initial commit: ICEIB IEEE Overleaf template\n"
    "dcde4e8 加入 myRef 資料夾（移除其原本的 .git，併入主 repo）\n"
    "6ba852f 新增：300字專業摘要套用 A2Z Outline 格式之 .tex 檔案\n"
    "d8198f4 移除 myRef 中不存在的殘留檔案記錄\n"
    "21493ff 合併 Overleaf 檔案：豐富版 references.bib、英文完整版 300字專業摘要、main.tex.bk\n"
    "5391e4c 移除臨時 olcli sync 目錄，加入 .gitignore\n"
    "61d3db2 新增 A2Z 大綱對應總覽附錄表，使 .tex 達約 5 頁\n"
    "c8fd0fb 進一步調整行距與邊界至 2.0 倍行距\n"
    "adb54a7 新增承諾聲明與作者簡介章節\n"
    "ddc47bf 新增系統參數一覽表\n"
    "732c118 在附錄前插入強制分頁\n"
    "30a3459 修改字體為 mathptmx 以支援 Overleaf pdfLaTeX 編譯\n"
    "ab61444 更新作者資訊：WEN WEI CHENG, National Chung Hsing University\n"
    "d9661b9 更新作者 Email 為 wilber830915@gmail.com\n"
)

pdf.section_title("2.7 作者資訊更新")
pdf.body_text(
    "在 ICEIB_IEEE_Overleaf_Template/main.tex 與 myRef/300字專業摘要_A2Z_Outline_Overleaf英文版.tex 中，"
    "作者資訊統一更新為："
)
pdf.code_block(
    "WEN WEI CHENG\n"
    "Department of Computer Science, National Chung Hsing University\n"
    "Taiwan\n"
    "Email: wilber830915@gmail.com\n"
)

# ==================== 結語 ====================
pdf.add_page()
pdf.chapter_title(3, "總結與後續建議")

pdf.body_text("3.1 已完成項目")
pdf.bullet("GitHub 儲存庫已建立並同步：wilber830915/AIoT-DIC4-ICEIB2027")
pdf.bullet("Overleaf 專案 AIoT-DIC4 (ID: 6b06bb69668f4d5869443455) 已連接並同步檔案")
pdf.bullet("olcli 環境已安裝並認證成功 (Node.js v26.13.1 + @aloth/olcli v0.18.1)")
pdf.bullet("300字專業摘要_A2Z_Outline.tex 已擴充至約 5 頁內容")
pdf.bullet("作者資訊已統一更新為 WEN WEI CHENG / National Chung Hsing University / wilber830915@gmail.com")

pdf.body_text("3.2 後續建議")
pdf.bullet("在 Overleaf 網頁介面中將 Compiler 切換為 XeLaTeX，以正確編譯中文 .tex 檔案")
pdf.bullet("設定 OpenCode MCP 伺服器 (olcli-mcp)，即可透過 AI 助手直接操作 Overleaf 專案")
pdf.bullet("定期執行 olcli sync 保持本地與 Overleaf 雲端同步")
pdf.bullet("GitHub 作為主要版本控制，Overleaf 作為協作編輯與遠端編譯平台")

pdf.output("/Users/wilber/Desktop/中興資工/11501/物聯網應用與資料分析/L11_DIC4/OpenCode_Overleaf_整合計畫總結.pdf")
print("PDF 已生成：OpenCode_Overleaf_整合計畫總結.pdf")