ZIP_FILENAME ?= repository-init.zip
TEMPLATE_FILENAME ?= initial.template

AWS_REGION ?= eu-central-1
AWS_BUCKET_NAME := serverless-workshop-eu-central-1-init

bucket:
	@ if [[ `aws s3 ls | grep -e ' $(AWS_BUCKET_NAME)$$' | wc -l` -eq 1 ]]; then \
		echo "Bucket exists"; \
	else \
		aws s3 mb s3://$(AWS_BUCKET_NAME); \
	fi
	@ aws s3api put-bucket-policy --bucket $(AWS_BUCKET_NAME) --policy file://bucket_policy.json

init: clean bucket
	@ (cd workshop-files && zip ../$(ZIP_FILENAME) -r *)
	@ aws s3 cp $(ZIP_FILENAME) s3://$(AWS_BUCKET_NAME)/$(ZIP_FILENAME)

deploy: bucket
	@ aws s3 cp $(TEMPLATE_FILENAME) s3://$(AWS_BUCKET_NAME)/$(TEMPLATE_FILENAME)

clean:
	@ rm -f $(ZIP_FILENAME) || true
