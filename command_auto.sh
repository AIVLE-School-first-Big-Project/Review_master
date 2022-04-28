#! /bin/bash

echo "input feature branch name : "
read feature

git checkout -b $feature develop
git add .

read -p "Commit 메서지를 입력해주세요 : " commit_message

git commit -m "$commit_message"

git checkout develop

echo "지금부터 develop 브랜치로 이동해 원격 develop와 pull을 진행하겠습니다. 충돌 발생시 직접 해결해주세요."
git pull origin develop

echo "..."
echo "지금부터 develop 브랜치와 Feature 브랜치를 Merge 시키도록 하겠습니다."
git merge --no-ff $feature

echo "Merge 성공"
echo "..."
echo "원격 서버에 develop 브랜치에 업로드하겠습니다."
git push origin develop

echo "위 작업이 성공적으로 완료 되었습니다."

