# 🎯 TalentScan — ATS Intelligent

> Analyseur de CV intelligent propulsé par l'IA — extraction OCR, matching de compétences et recommandations recruteur.

---

## ✨ Fonctionnalités

- **OCR Vision IA** : Lit les CVs Canva, PDFs imagés, captures d'écran et documents scannés
- **Analyse sémantique** : Comprend le contexte réel du CV, pas seulement des mots-clés
- **Score pondéré sur 5 critères** : Compétences techniques, Expérience, Formation, Soft Skills, Adéquation poste
- **Traitement hybride** : Extraction texte + Vision OCR avec fallback automatique
- **Rapport complet** : Points forts, lacunes, red flags, recommandations recruteur et décision finale
- **Export JSON** du rapport d'analyse

---

## 📁 Structure du projet

```
talentscan/
├── app.py                      ← Application principale Streamlit
├── requirements.txt            ← Dépendances Python
├── README.md                   ← Ce fichier
├── .gitignore                  ← Fichiers exclus de Git
└── .streamlit/
    └── secrets.toml            ← Clé API (local uniquement, jamais sur GitHub)
```

---

## 🚀 Installation locale

```bash
# 1. Cloner le repository
git clone https://github.com/VOTRE_USER/talentscan.git
cd talentscan

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer la clé API
# Créez le fichier .streamlit/secrets.toml et ajoutez votre clé API

# 4. Lancer l'application
streamlit run app.py
```

---

## ☁️ Déploiement sur Streamlit Cloud (Gratuit)

### 1. Mettre le code sur GitHub

```bash
git init
git add app.py requirements.txt README.md .gitignore
git commit -m "Initial commit — TalentScan ATS"
git branch -M main
git remote add origin https://github.com/VOTRE_USER/talentscan.git
git push -u origin main
```

### 2. Déployer

1. Allez sur **https://share.streamlit.io**
2. Connectez votre compte GitHub
3. Cliquez **"New app"**
4. Sélectionnez votre repository et `app.py`
5. Cliquez **"Deploy"**

### 3. Configurer la clé API

Dans Streamlit Cloud → **App Settings → Secrets**, ajoutez :

```toml
API_KEY = "votre_cle_api"
```

Votre application sera accessible sur `https://votre-app.streamlit.app` 🎉

---

## 📄 Formats de CV supportés

| Format | Support | Mode |
|--------|---------|------|
| PDF standard (texte) | ✅ | Extraction directe |
| PDF Canva / imagé | ✅ | Vision IA |
| DOCX / DOC | ✅ | Extraction directe |
| PNG / JPG / WEBP | ✅ | Vision IA |

---

## 🏗️ Architecture technique

```
Fichier uploadé
    │
    ├── PDF texte riche ──────── Extraction PyMuPDF ──────── Analyse IA
    │
    ├── PDF imagé / Canva ─────── Conversion en images ────── Vision IA
    │
    ├── DOCX ─────────────────── Extraction python-docx ───── Analyse IA
    │
    └── Image PNG/JPG ──────────────────────────────────────── Vision IA
```

---

## 💡 Conseils d'utilisation

- **Description du poste** : Plus elle est détaillée (40+ mots), meilleur est le matching
- **CVs Canva** : Exportez directement en PDF depuis Canva, la Vision IA s'en charge
- **Images scannées** : Privilégiez une bonne qualité (300 DPI minimum)
- **Interprétation du score** : 70%+ → À interviewer · 45–70% → Potentiel · <45% → Non prioritaire

---

## 🔒 Sécurité & Confidentialité

- Aucune donnée stockée — tout est traité en mémoire
- La clé API est gérée via les Secrets Streamlit, jamais dans le code
- Le fichier `.gitignore` exclut automatiquement les fichiers sensibles

---

*Développé avec Streamlit · Vision IA · Python*
