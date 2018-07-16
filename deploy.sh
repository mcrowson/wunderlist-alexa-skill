docker pull lambci/lambda:build-python3.6
docker run -v ~/.aws/:/root/.aws -v $(pwd):/var/task --rm lambci/lambda:build-python3.6 bash -c "
python3 -m venv lambda_env
lambda_env/bin/pip install -r requirements.txt
zip lambda_code.zip app.py
cd lambda_env/lib/python3.6/site-packages
zip -r ../../../../lambda_code.zip ./
cd ../../../lib64/python3.6/site-packages
zip -r ../../../../lambda_code.zip ./
cd ../../../../
rm -rf lambda_env
"

aws lambda update-function-code --function-name wunderlist --zip-file fileb://lambda_code.zip
rm lambda_code.zip
