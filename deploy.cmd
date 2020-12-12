@echo off
:: Deploy on GitHub automatic...

set /p commit="Type a description of commit: "

git add .
git commit -m "%commit%"
git push origin master

echo "Commited!"

timeout 5 > NUL

heroku logs --tail -a developersbrasil