# ⚡ QUICK START - CRA Payroll Tool
## From Download to Deployed in 20 Minutes

---

## 📥 STEP 1: DOWNLOAD FILES (2 min)

From this Claude.ai chat, download:
- ✅ app.py
- ✅ requirements.txt  
- ✅ employees.csv
- ✅ CLAUDE_CODE_HANDOFF.md (detailed guide)
- ✅ STREAMLIT_DEPLOYMENT_GUIDE.md (deployment steps)

---

## 💻 STEP 2: OPEN CLAUDE CODE (1 min)

```bash
# Launch Claude Code CLI
claude-code

# Or open Claude Code desktop app
```

---

## 📁 STEP 3: SET UP PROJECT (3 min)

```bash
# Create project folder
mkdir ~/cra-payroll-automation
cd ~/cra-payroll-automation

# Move downloaded files here
# (drag & drop or copy them)

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🧪 STEP 4: TEST LOCALLY (5 min)

```bash
# Run the app
streamlit run app.py

# Browser opens at http://localhost:8501
# Upload employees.csv
# Click "Calculate Payroll"
# Download Excel file
# ✅ If it works, proceed to deploy!
```

---

## 🌐 STEP 5: DEPLOY TO GITHUB (5 min)

```bash
# Initialize git
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub.com:
# - Go to github.com/new
# - Name: cra-payroll-automation
# - Public repo
# - Don't initialize
# - Create

# Push (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/cra-payroll-automation.git
git branch -M main
git push -u origin main
```

---

## ☁️ STEP 6: DEPLOY TO STREAMLIT (4 min)

**Via browser (can't automate):**

1. Go to **https://streamlit.io/cloud**
2. **Sign in with GitHub**
3. Click **"New app"**
4. Select:
   - Repository: `cra-payroll-automation`
   - Branch: `main`
   - Main file: `app.py`
   - App URL: `cra-payroll` (or your choice)
5. Click **"Deploy"**
6. Wait 2-3 minutes
7. ✅ **Done! Get your URL:** `https://cra-payroll.streamlit.app`

---

## 📧 STEP 7: SHARE WITH FRIEND

```
Subject: CRA Payroll Tool is Live!

Hey [Friend],

The CRA payroll automation is ready:
🔗 https://cra-payroll.streamlit.app

Just upload a CSV, get instant Excel reports.
Try it and let me know what you think!

Attached: CSV template

[Your name]
```

---

## 🐛 TROUBLESHOOTING

**Can't install packages?**
```bash
pip install --upgrade pip
pip install streamlit pandas openpyxl
```

**Port 8501 in use?**
```bash
streamlit run app.py --server.port 8502
```

**Git push rejected?**
```bash
git pull origin main --rebase
git push
```

---

## 📞 NEED HELP IN CLAUDE CODE?

Paste this to start conversation:

```
I'm deploying a CRA payroll automation tool (Streamlit app).

Files: app.py, requirements.txt, employees.csv
Goal: Test locally, then deploy to Streamlit Cloud

Current issue: [describe what's not working]
```

---

## ✅ SUCCESS = 

- ✅ App runs locally
- ✅ Code on GitHub  
- ✅ Live at: https://[yourname].streamlit.app
- ✅ Friend can access it
- ✅ Total cost: $0

**Time: 20 minutes | Cost: $0 | Risk: Zero**

---

## 📚 FULL DOCS

- **CLAUDE_CODE_HANDOFF.md** - Complete context & troubleshooting
- **STREAMLIT_DEPLOYMENT_GUIDE.md** - Detailed deployment steps
- **MONETIZATION_PLAN.md** - Business strategy

---

**Ready? Download files → Open Claude Code → Follow steps above!** 🚀
