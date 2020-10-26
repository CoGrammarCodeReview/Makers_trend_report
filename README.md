# Makers_trend_report
Script to generate trend reports for Makers Academy.


Trend reports are provided by us to Makers every two weeks on a Monday.

Process:
* Go to https://airtable.com/shrwOi72LcgFIdRR5/tblWkpfb3H87FreC3
* Select download CSV from the … tab.
* Rename the csv to ‘trends’
* Open the “makers_trends.py” file.
* Set the dates to calculate the report for:
* The first date should be the Monday of the last two-week cycle
* The second date should be the Monday of the next two-week cycle (which is excluded)
* Run the script.
* Open trends_report.txt
* You will have to manually filter the students flagged for attention.
  *  Go back to the external airtable
  *  Hit the filter tab, select by ‘review’
  *  For each flagged ID, filter by review and remove from the list if: if they have only done one review (and not manually flagged for attention on the slack channel), if they have shown improvement in a subsequent review.
* Search your email for 'review cancelled' and append 'Cancellations: <cancellation_count> to the 'General' rubric.
* Create a post in the Slack channel.
* Paste the report and format it nicely.
