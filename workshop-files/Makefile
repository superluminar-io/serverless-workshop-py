AWS_REGION ?= eu-central-1
FE_REPO_NAME := serverless-workshop-fe

test:
	@:

fe-bucket: guard-FE_BUCKET_NAME
	@ if [ `aws s3 ls | grep -e ' $(FE_BUCKET_NAME)$$' | wc -l` -eq 1 ]; then \
		echo "Bucket exists"; \
	else \
		aws s3 mb s3://$(FE_BUCKET_NAME) --region $(AWS_REGION); \
	fi

fetch-frontend:
	rm -rf frontend
	wget https://github.com/superluminar-io/$(FE_REPO_NAME)/archive/master.zip -O master.zip
	unzip master.zip
	rm -f master.zip
	mv $(FE_REPO_NAME)-master frontend

deploy-frontend: fe-bucket
	(cd frontend && npm install)
	(cd frontend && npm run-script build)
	(cd frontend && aws s3 sync build/ s3://$(FE_BUCKET_NAME) --delete --acl public-read)
	@ echo
	@ echo
	@ echo "https://$(FE_BUCKET_NAME).s3.$(AWS_REGION).amazonaws.com/index.html"
	@ echo
	@ echo

guard-%:
	@ if [ -z '${${*}}' ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

deploy:
	@ pip install -r preview/requirements.txt -t preview
	@ pip install -r create_url/requirements.txt -t create_url
	@ pip install -r get_url/requirements.txt -t get_url
	@ sam deploy

.PHONY: test deploy fe-bucket fetch-frontend deploy-frontend
