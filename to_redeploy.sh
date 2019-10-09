# to rebuild image and redeploy in heroku
# don't forget to login to heroku container registry first
docker build -t zhunt/october .
docker tag zhunt/october registry.heroku.com/zdna/web
docker push registry.heroku.com/zdna/web
docker container:push web
heroku container:release web
