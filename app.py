from flask import Flask, render_template, Response
app = Flask(__name__)

# Solution from here: https://stackoverflow.com/a/49334973

#rendering the HTML page which has the button
@app.route('/')
def root():
    return render_template('button.html')

#rendering the HTML page which has the button
@app.route('/log')
def log():
    with open("app.log") as logfile:
        logtext = logfile.read()
    return Response(logtext, mimetype='text/plain')

@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    return "Test complete"

@app.route('/run_the_algorithm')
def run_the_algorithm():
    import run
    run.run()
    return "Run complete"

if __name__ == '__main__':
    app.run(debug = False, host="0.0.0.0")

