from flask import Flask, render_template, Response, request
app = Flask(__name__)

# Solution from here: https://stackoverflow.com/a/49334973

# Health check
@app.route('/healthz')
def healthz():
    return "OK", 200  # returns OK

# Page 0: select the language
@app.route('/')
def root():
    return render_template('0.html')

class algorithms:
    import run_bounded_sharing   as bounded_sharing
    import run_course_allocation as course_allocation


# Page 1: select spreadsheet and algorithm
@app.route('/1/<lang>')
def step1(lang:str):
    return render_template(f'1-{lang}.html', lang=lang, algorithm_names=["bounded_sharing", "course_allocation"])

@app.route('/2/<lang>')
def step2(lang:str):
    url = request.args.get('url')
    print("url=",url)
    algorithm_name = request.args.get('algorithm_name')
    print("algorithm_name=",algorithm_name)
    error = None
    try:
        import gspread
        account = gspread.service_account("credentials.json")
        print("account=",account)
        spreadsheet = account.open_by_url(url)
        print("spreadsheet=",spreadsheet)
    except gspread.exceptions.APIError:
        error = "Google Spreadsheet API error! Please verify that you shared your spreadsheet with the above address."
    except gspread.exceptions.NoValidUrlKeyFound:
        error = "Google Spreadsheet could not find a key in your URL! Please check that the URL you entered points to a valid spreadsheet."
    except gspread.exceptions.SpreadsheetNotFound:
        error = "Google Spreadsheet could not find the spreadsheet you entered! Please check that the URL points to a valid spreadsheet."
    except FileNotFoundError as e:
        error = f"File not found: {e.filename}."
    except Exception as e:
        error = str(e) + "! Please check your URL and try again."
    if error is not None:
        print("error=",error)
        return render_template(f'1-{lang}.html', error=error, lang=lang)
    else:
        return render_template(f'2-{lang}.html', url=url, lang=lang, algorithm_name=algorithm_name)


@app.route('/run/<algorithm_name>')
def run_algorithm(algorithm_name:str):
    algorithm = getattr(algorithms, algorithm_name)
    url = request.args.get('url')
    lang = request.args.get('lang')
    print("url=",url, "lang=",lang)
    algorithm.run(url=url, language=lang)
    return "Run complete"


# Viewing the log file
@app.route('/log')
def log():
    with open("app.log") as logfile:
        logtext = logfile.read()
    return Response(logtext, mimetype='text/plain')

# Testing background process
@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    return "Test complete"

if __name__ == '__main__':
    # app.run(debug = True)
    app.run(debug = False, host="0.0.0.0")

