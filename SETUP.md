# Setup Guide

Complete setup instructions for Agent B - AI Workflow Capture System.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18 or higher** - [Download Node.js](https://nodejs.org/)
- **OpenAI API Key** - [Get API Key](https://platform.openai.com/api-keys)
- **Git** - [Download Git](https://git-scm.com/)

### Verify Prerequisites

```bash
# Check Python version
python3 --version  # Should be 3.11+

# Check Node.js version
node --version     # Should be v18+

# Check npm version
npm --version      # Should be 9+
```

## Quick Start

### Automated Setup (Recommended)

This is the fastest way to get started. The setup scripts handle everything automatically.

#### Backend Setup

```bash
cd backend

# Make the script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

The script will:

1. Create a Python virtual environment
2. Install all Python dependencies
3. Install Playwright browsers
4. Create necessary directories
5. Create a `.env` file template

After the script completes:

```bash
# Edit .env and add your OpenAI API key
nano .env
# Add: OPENAI_API_KEY=sk-your-key-here

# Activate the virtual environment
source venv/bin/activate

# Start the backend server
python main.py
```

✅ Backend is now running at: `http://localhost:8000`

#### Frontend Setup

Open a new terminal window:

```bash
cd frontend

# Make the script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

The script will:

1. Install all Node.js dependencies
2. Create a `.env.local` file with default settings

After the script completes:

```bash
# Start the frontend development server
npm run dev
```

✅ Frontend is now running at: `http://localhost:3000`

### Manual Setup

If you prefer to set things up manually or the automated scripts don't work on your system.

#### Backend Manual Setup

```bash
cd backend

# 1. Create a Python virtual environment
python3 -m venv venv

# 2. Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install chromium

# 5. Install system dependencies for Playwright (may require sudo)
# On macOS:
# (Usually not needed if you have Xcode command line tools)

# On Linux:
# playwright install-deps chromium

# On Windows:
# (Usually not needed)

# 6. Create .env file
touch .env

# 7. Add your OpenAI API key to .env
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# 8. Create directory for screenshots
mkdir -p screenshots

# 9. Start the backend server
python main.py
```

✅ Backend is now running at: `http://localhost:8000`

#### Frontend Manual Setup

Open a new terminal window:

```bash
cd frontend

# 1. Install Node.js dependencies
npm install

# 2. Create .env.local file
touch .env.local

# 3. Add backend API URL
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" >> .env.local

# 4. Start the development server
npm run dev
```

✅ Frontend is now running at: `http://localhost:3000`

## Environment Variables

### Backend Environment Variables

The backend requires an `.env` file in the `backend/` directory.

**Required:**

- `OPENAI_API_KEY` - Your OpenAI API key

**Optional:**

- `HOST` - Server host (default: `0.0.0.0`)
- `PORT` - Server port (default: `8000`)
- `ENVIRONMENT` - Environment mode (default: `development`)

**Example `.env` file:**

```env
# Required
OPENAI_API_KEY=sk-proj-abc123xyz789...

# Optional
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development
```

For detailed information about environment variables, see [backend/ENV.md](backend/ENV.md).

### Frontend Environment Variables

The frontend requires an `.env.local` file in the `frontend/` directory.

**Required:**

- `NEXT_PUBLIC_API_URL` - Backend API URL

**Example `.env.local` file:**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Getting an OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to the [API Keys](https://platform.openai.com/api-keys) section
4. Click "Create new secret key"
5. Copy the key (you won't be able to see it again!)
6. Add it to your `backend/.env` file

**Note**: OpenAI API usage requires a paid account with available credits.

## Verifying Installation

### Test Backend

1. **Check the health endpoint:**

```bash
curl http://localhost:8000
```

Expected response:

```json
{
  "service": "Agent B - Workflow Capture System",
  "status": "running"
}
```

2. **Check backend logs:**
   Look for these messages in your backend terminal:

```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Test Frontend

1. **Open in browser:**
   Navigate to `http://localhost:3000`

2. **Expected UI:**

- You should see the "Agent B" heading
- Workflow capture form with input fields
- Example tasks section
- Info cards about features

### Test Complete System

Run a simple workflow to verify everything works:

1. Open `http://localhost:3000` in your browser
2. Enter task: `How do I search on Google?`
3. Leave login URL empty (Google doesn't require login)
4. Session file name: `google_session.json`
5. Click "Start Capture"
6. Wait 30-60 seconds
7. You should see captured workflow with screenshots

## Development Workflow

When developing, you'll typically run both backend and frontend simultaneously.

### Terminal 1: Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

The backend will auto-reload when you modify Python files (if you're using `uvicorn --reload`).

### Terminal 2: Frontend

```bash
cd frontend
npm run dev
```

The frontend will auto-reload when you modify React components.

## Troubleshooting

### Common Backend Issues

#### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:** Make sure you've activated the virtual environment and installed dependencies:

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue: "playwright: command not found"

**Solution:** Install Playwright browsers:

```bash
cd backend
source venv/bin/activate
playwright install chromium
```

#### Issue: "OpenAI API error: Incorrect API key provided"

**Solution:**

1. Check that your `.env` file exists in the `backend/` directory
2. Verify the API key is correct (no extra spaces or quotes)
3. Ensure the key starts with `sk-`
4. Check your OpenAI account has available credits

#### Issue: "Port 8000 already in use"

**Solution:** Kill the process using port 8000:

```bash
# On macOS/Linux:
lsof -ti:8000 | xargs kill -9

# On Windows:
# netstat -ano | findstr :8000
# taskkill /PID <PID> /F
```

Or change the port in `.env`:

```env
PORT=8001
```

#### Issue: "Target page, context or browser has been closed"

**Solution:** This usually happens if the browser crashes. Restart the backend server:

```bash
# Press Ctrl+C to stop
# Then restart:
python main.py
```

### Common Frontend Issues

#### Issue: "Cannot connect to backend"

**Solution:**

1. Verify backend is running: `curl http://localhost:8000`
2. Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
3. Restart frontend: `npm run dev`

#### Issue: "Module not found" errors

**Solution:** Reinstall dependencies:

```bash
cd frontend
rm -rf node_modules
rm package-lock.json
npm install
```

#### Issue: "Port 3000 already in use"

**Solution:** Use a different port:

```bash
PORT=3001 npm run dev
```

#### Issue: "Build errors" or "Type errors"

**Solution:** Clear Next.js cache:

```bash
cd frontend
rm -rf .next
npm run dev
```

### Playwright-Specific Issues

#### Issue: Playwright browser won't launch

**Solution:** Install system dependencies:

```bash
# On Ubuntu/Debian:
sudo apt-get install libgbm1

# On macOS:
# Usually works out of the box with Xcode command line tools

# On Windows:
# Usually works out of the box
```

#### Issue: "Browser closed unexpectedly"

**Solution:**

1. Try reinstalling Playwright browsers:

```bash
cd backend
source venv/bin/activate
playwright install --force chromium
```

2. Check available disk space (Playwright needs ~500MB per browser)

3. Try running with headed browser for debugging:
   - Edit `session.py` and change `headless=False` to `headless=True`

## Building for Production

### Backend Production Build

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Install Playwright
playwright install chromium

# Run with production settings
export ENVIRONMENT=production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend Production Build

```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Start production server
npm start
```

## Running Tests

### Backend Tests

```bash
cd backend
source venv/bin/activate

# Run API tests (if available)
python -m pytest tests/

# Or manual API test
python test_api.py
```

### Frontend Tests

```bash
cd frontend

# Run TypeScript type checking
npm run type-check

# Run linting
npm run lint

# Run tests (if available)
npm test
```

## Updating Dependencies

### Backend Dependencies

```bash
cd backend
source venv/bin/activate

# Update all packages
pip install --upgrade -r requirements.txt

# Or update specific package
pip install --upgrade openai
```

### Frontend Dependencies

```bash
cd frontend

# Check for outdated packages
npm outdated

# Update all packages
npm update

# Or update specific package
npm install next@latest
```

## Next Steps

After successful setup:

1. ✅ Read [README.md](README.md) for an overview
2. ✅ Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
3. ✅ Try example workflows in the UI
4. ✅ Check [backend/ENV.md](backend/ENV.md) for environment configuration
5. ✅ Start building your own workflows!

## Support

If you encounter issues not covered here:

1. Check the [ARCHITECTURE.md](ARCHITECTURE.md) for system details
2. Review backend logs for error messages
3. Check Playwright documentation: https://playwright.dev
4. Check CrewAI documentation: https://docs.crewai.com
5. Check FastAPI documentation: https://fastapi.tiangolo.com
6. Check Next.js documentation: https://nextjs.org/docs

## Tips for Success

1. **Start Simple** - Test with simple websites (Google, Wikipedia) first
2. **Check Logs** - Backend logs show agent reasoning and errors
3. **Use Verbose Mode** - Agents log their decisions when `verbose: true`
4. **Session Files** - Reuse session files to avoid repeated logins
5. **Screenshots** - Check `backend/screenshots/` to debug visual issues

---

**Happy workflow capturing! 🎉**

If everything is set up correctly, you should now be able to capture workflows from any web application!
