#!/bin/bash

echo "🚀 Setting up Agent B Frontend..."

# Install dependencies
echo "📦 Installing Node dependencies..."
npm install

# Copy .env.local.example if it doesn't exist
if [ ! -f .env.local ]; then
    echo "⚙️  Creating .env.local file..."
    cp .env.local.example .env.local
fi

echo "✅ Frontend setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure the backend is running on http://localhost:8000"
echo "2. Run the frontend: npm run dev"
echo "3. Open http://localhost:3000 in your browser"

