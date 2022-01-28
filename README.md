## An invoice HTML viewer

It is very likely that most small entrepreneurs have their invoice system on the cloud. And that's perfectly reasonable given
that we rely on so many things that are 'just' online. Hence, myself as an entrepreneur had to keep order of the invoices, payments
and so on...

I present you your very own fully-customizable invoice HTML viewer.

!!! . This assumes you have your invoices stored in sheets and are able to export them to csv.

### Prerequisities
You should have your invoices stored on the PC within a reasonable structure
For instance, take a look at the mapping function in the `build.py (line 90)`

### How to start
A) You are using GoogleSheets
1. Make your sheets shareable by link only
2. Copy the generate so called 'invite' link. This should look something like this
 `https://docs.google.com/spreadsheets/d/<doc_id>/edit#gid=<gid>`
3. Head over to the key.sh and set the value of <doc_id>
4. Head over to the fetch.sh and set the mapping for the individual sheets
```sh
YEAR_MAP=([2020]=0 [2021]=1796467941 [2022]=1875813237)
```
5. `source fetch.sh`

B) You have your data directly in `csv` format
1. Store the csv files in the /csv folder, if missing create
2. Call the `python3` script which will build the files
```python3
python3 build.py csv/2020.csv
```
3. The rendered html page resides in `/public/` folder

!!! . You have a fully-customizable HTML invoice viewer at your disposal. Run it on localhost / Distribute / Modify...