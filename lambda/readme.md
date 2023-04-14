# How to Use
- Use v2, not v1. v1 is only there in case v2 no longer works.
- Create an S3 bucket
- Create a Lambda function with the code
  - After creating the Lambda function, it won't run the code because it doesn't have the necessary libraries, follow this [guide](https://repost.aws/knowledge-center/lambda-import-module-error-python) and download the libraries imported in the function
  - To upload to your S3 bucket, go to your Lambda function, Configuration, Environment variables, then set the key to "BUCKET_NAME" and the value to your S3 bucket.
- Create an Eventbridge rule that activates at least every 10 minutes (not less otherwise Steam will temp ban the IP)
- Connect Eventbridge rule to Lambda function when ready to start scraping

# Example Output (of csv file)
## [LOB Scraper](https://github.com/replacementAI/CSGO-Steam-Market-Scrapers/blob/main/lambda/LOB%20Scraper%20v2.py)
| buy_price | buy_volume | sell_price | sell_volume |
|------------|-------------|-------------|-------------|
| 2.61       | 7           | 2.69        | 1           |
