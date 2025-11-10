#!/bin/bash
# Show Project Activity (alle Branches)

echo "============================================================"
echo "📊 CNC-ToolCalc Project Activity"
echo "============================================================"
echo ""

# Update from remote
echo "🔄 Fetching latest from GitHub..."
git fetch --all -q
echo ""

# Show today's commits
echo "📅 Commits heute ($(date +%Y-%m-%d)):"
echo "---"
git log --all --since="today" --pretty=format:"%h %Cgreen%an%Creset %ad %Cblue%s%Creset" --date=short
echo ""
echo ""

# Show changed files today
echo "📁 Geänderte Dateien heute:"
echo "---"
git log --all --since="today" --name-only --pretty=format:"" | sort | uniq | head -20
echo ""
echo ""

# Show branch status
echo "🌳 Branch Status:"
echo "---"
git branch -a | grep -E "agent|main|develop"
echo ""

# Show latest commit per agent branch
echo "🤖 Agent Status (letzter Commit):"
echo "---"
echo "Backend:  $(git log agent/backend-calculation --oneline -1)"
echo "Frontend: $(git log agent/frontend-workflow --oneline -1)"
echo "UI:       $(git log agent/ui-specialist --oneline -1)"
echo "Main:     $(git log main --oneline -1)"
echo ""

# Show files changed on each agent branch (vs main)
echo "📊 Änderungen pro Agent (vs main):"
echo "---"
echo "Backend:  $(git diff --shortstat main..agent/backend-calculation)"
echo "Frontend: $(git diff --shortstat main..agent/frontend-workflow)"
echo "UI:       $(git diff --shortstat main..agent/ui-specialist)"
echo ""

echo "============================================================"
echo "✅ Activity Report Complete"
echo "============================================================"
