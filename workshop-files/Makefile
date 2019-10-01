PROJECT := url-shortener

AWS_BUCKET_NAME := $(PREFIX)-$(PROJECT)-artifacts
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

package: bucket guard-PREFIX
	@ mkdir -p dist
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

outputs-%:
	@ QUERY="(Stacks[0].Outputs[?OutputKey=='$*'].OutputValue)[0]" \
		FORMAT=text \
		$(MAKE) describe

guard-%:
	@ if [ -z '${${*}}' ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

.PHONY: test configure package deploy describe outputs
