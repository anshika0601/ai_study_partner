from datetime import date, datetime, timedelta


DATE_FMT = "%d-%m-%Y"




def today_str() -> str:
 return date.today().strftime(DATE_FMT)




def tomorrow_str() -> str:
 return (date.today() + timedelta(days=1)).strftime(DATE_FMT)




def date_to_str(d: date) -> str:
 return d.strftime(DATE_FMT)




def str_to_date(s: str) -> date:
 return datetime.strptime(s, DATE_FMT).date()