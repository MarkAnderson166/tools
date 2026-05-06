#!/usr/bin/env bash

set -e

echo "Installing git boom alias..."

mkdir -p ~/.local/bin

cat > ~/.local/bin/git-boom <<'EOF'
#!/usr/bin/env bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

MESSAGE="$*"

if [ -z "$MESSAGE" ]; then
    echo -e "${RED}Usage:${NC} git boom 'commit message'"
    exit 1
fi

echo
echo -e "${CYAN}=============================="
echo -e "        GIT STATUS"
echo -e "==============================${NC}"
git status
echo

read -p "$(echo -e ${YELLOW}"Continue with add/commit/pull/push? (y/N): "${NC})" CONFIRM

case "$CONFIRM" in
    y|Y|yes|YES)
        ;;
    *)
        echo -e "${RED}Cancelled.${NC}"
        exit 0
        ;;
esac

echo
echo -e "${BLUE}Adding files...${NC}"
git add .

echo -e "${BLUE}Committing...${NC}"
git commit -m "$MESSAGE"

echo -e "${BLUE}Pulling latest...${NC}"
git pull

echo -e "${BLUE}Pushing...${NC}"
git push

echo
echo -e "${GREEN}Boom complete.${NC}"
EOF

chmod +x ~/.local/bin/git-boom

# Ensure ~/.local/bin is in PATH
if ! grep -q 'PATH="$HOME/.local/bin:$PATH"' ~/.bashrc; then
    echo '' >> ~/.bashrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi

# Git alias
git config --global alias.boom '!git-boom'

echo
echo "Setup complete."
echo "Restart terminal or run:"
echo "source ~/.bashrc"
echo
echo "Then use:"
echo "git boom 'your commit message'"
