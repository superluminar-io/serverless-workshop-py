PROJECT := url-shortener

AWS_BUCKET_NAME := $(PREFIX)-$(PROJECT)-artifacts
FE_BUCKET_NAME := $(PREFIX)-$(PROJECT)-fe
AWS_STACK_NAME := $(PREFIX)-$(PROJECT)-stack
AWS_REGION ?= eu-central-1

FILE_TEMPLATE = ./template.yaml
FILE_PACKAGE = ./dist/stack.yml

test:
	@:

bucket: guard-PREFIX
	@ if [ `aws s3 ls | grep -e ' $(AWS_BUCKET_NAME)$$' | wc -l` -eq 1 ]; then \
		echo "Bucket exists"; \
	else \
		aws s3 mb s3://$(AWS_BUCKET_NAME) --region $(AWS_REGION); \
	fi

fe-bucket: guard-PREFIX
	@ if [ `aws s3 ls | grep -e ' $(FE_BUCKET_NAME)$$' | wc -l` -eq 1 ]; then \
		echo "Bucket exists"; \
	else \
		aws s3 mb s3://$(FE_BUCKET_NAME) --region $(AWS_REGION); \
	fi

package: bucket guard-PREFIX
	@ mkdir -p dist
	@ pip install -r preview/requirements.txt -t preview
	@ pip install -r create_url/requirements.txt -t create_url
	@ pip install -r get_url/requirements.txt -t get_url
	@ aws cloudformation package \
		--template-file $(FILE_TEMPLATE) \
		--s3-bucket $(AWS_BUCKET_NAME) \
		--output-template-file $(FILE_PACKAGE) \
		--region $(AWS_REGION)

deploy: guard-PREFIX
	@ aws cloudformation deploy \
		--template-file $(FILE_PACKAGE) \
		--region $(AWS_REGION) \
		--capabilities CAPABILITY_IAM \
		--stack-name $(AWS_STACK_NAME) \
		--force-upload
destroy:
	@ aws cloudformation delete-stack \
		--stack-name $(AWS_STACK_NAME) \

describe:
	@ aws cloudformation describe-stacks --stack-name $(AWS_STACK_NAME) \
		$(if $(value QUERY), --query "$(QUERY)",) \
		$(if $(value FORMAT), --output "$(FORMAT)",)

fetch-frontend:
	rm -rf frontend
	wget https://github.com/superluminar-io/sac-workshop-fe/archive/master.zip -O master.zip
	unzip master.zip
	rm -f master.zip
	mv sac-workshop-fe-master frontend

deploy-frontend: fe-bucket
	(cd frontend && npm install)
	(cd frontend && npm run-script build)
	(cd frontend && aws s3 sync build/ s3://$(FE_BUCKET_NAME) --delete --acl public-read)
	@ echo
	@ echo
	@ echo "https://$(FE_BUCKET_NAME).s3.$(AWS_REGION).amazonaws.com/index.html"
	@ echo
	@ echo

outputs-%:
	@ QUERY="(Stacks[0].Outputs[?OutputKey=='$*'].OutputValue)[0]" \
		FORMAT=text \
		$(MAKE) describe

guard-%:
	@ if [ -z '${${*}}' ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

.PHONY: test configure package deploy describe outputs fetch-frontend deploy-frontend
