# Setup Instructions: Create GitHub Repository for QuizTonic API

This document provides step-by-step instructions to create and initialize the GitHub repository for `quiztonic_api`.

## 📋 Prerequisites

- GitHub account with repository creation permissions
- Git installed locally
- All files copied to `/Users/baptisteveyrard/Local/GitHub/RAQAM/quiztonic_api/`

## 🚀 Steps to Create GitHub Repository

### 1. Create Repository on GitHub

1. Go to [GitHub](https://github.com)
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the repository details:
   - **Repository name**: `quiztonic_api`
   - **Description**: `QuizTonic API - Backend service for AI-powered quiz and flashcard generation`
   - **Visibility**: Choose **Public** or **Private** (recommend Private for production)
   - **Initialize repository**: ❌ **DO NOT** check "Add a README file"
   - **Add .gitignore**: ❌ Leave as "None"
   - **Choose a license**: Optional (MIT recommended)
5. Click **"Create repository"**

### 2. Initialize Local Git Repository

Open a terminal and navigate to the quiztonic_api directory:

```bash
cd /Users/baptisteveyrard/Local/GitHub/RAQAM/quiztonic_api
```

Initialize Git and make initial commit:

```bash
# Initialize Git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: QuizTonic API separated from main project

- Renamed from RAQAM-API to quiztonic_api
- Updated all references and deployment scripts
- Added API_CONTRACT.md for API documentation
- Added MIGRATION.md for migration guide
"

# Add remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/Bptmn/quiztonic_api.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

### 3. Verify Repository

1. Go to your GitHub repository page
2. Verify all files are present:
   - ✅ `README.md`
   - ✅ `API_CONTRACT.md`
   - ✅ `MIGRATION.md`
   - ✅ `deploy_lambda_url.sh`
   - ✅ `requirements.txt`
   - ✅ `Dockerfile`
   - ✅ `src/` directory
   - ✅ `api/` directory
   - ✅ `config/` directory

### 4. Set Up Repository Settings

On the GitHub repository page:

1. Go to **Settings** → **General**
2. Scroll to **Features**
   - ✅ Enable **Issues**
   - ✅ Enable **Projects**
   - ✅ Enable **Wiki** (optional)
3. Go to **Settings** → **Branches**
   - Add branch protection rule for `main` branch:
     - ✅ Require pull request reviews
     - ✅ Require status checks
     - ✅ Require branches to be up to date
4. Go to **Settings** → **Secrets and variables** → **Actions**
   - Add secrets if needed for CI/CD:
     - `OPENAI_API_KEY`
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_ACCESS_KEY`

### 5. Update README Links

After creating the repository, update the links in `README.md` and `API_CONTRACT.md`:

1. ✅ Links updated: `https://github.com/Bptmn/quiztonic_api`
2. ✅ Links updated: `https://github.com/Bptmn/quiztonic`

### 6. Create Initial Release

Create a v1.0.0 release:

```bash
# Create and push a tag
git tag -a v1.0.0 -m "Initial release: QuizTonic API v1.0.0"
git push origin v1.0.0
```

On GitHub:
1. Go to **Releases** → **Draft a new release**
2. Select tag `v1.0.0`
3. Title: `QuizTonic API v1.0.0`
4. Description: `Initial release of QuizTonic API separated from main project`
5. Click **"Publish release"**

## ✅ Checklist

- [ ] GitHub repository created
- [ ] Repository initialized locally
- [ ] Initial commit made
- [ ] Code pushed to GitHub
- [ ] All files verified in GitHub
- [ ] Repository settings configured
- [ ] Branch protection enabled
- [ ] Secrets added (if needed)
- [ ] README links updated
- [ ] Initial release created
- [ ] Team members added (if applicable)

## 🔗 Next Steps

After creating the repository:

1. **Update QuizTonic App**: Update the app to reference the new repository
2. **Deploy API**: Deploy the API to AWS Lambda using `deploy_lambda_url.sh`
3. **Update Documentation**: Update any project documentation that references the old RAQAM-API location
4. **Migrate Issues**: If you have issues in the old repository, migrate them to the new one
5. **Set Up CI/CD**: Consider setting up GitHub Actions for automated testing and deployment

## 📚 Related Documentation

- [Migration Guide](MIGRATION.md)
- [API Contract](API_CONTRACT.md)
- [Deployment Guide](RAQAM_LAMBDA_DEPLOYMENT_GUIDE.md)

## 🆘 Troubleshooting

### Error: Repository already exists
If you get an error that the repository already exists, either:
- Delete the existing repository on GitHub, or
- Use a different name for the repository

### Error: Authentication failed
Make sure you're authenticated with GitHub:
```bash
# Check Git configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Use SSH instead of HTTPS if needed
git remote set-url origin git@github.com:YOUR_USERNAME/quiztonic_api.git
```

### Error: Large files
If you have large files, consider:
- Adding them to `.gitignore`
- Using Git LFS for large files
- Removing unnecessary files before committing

