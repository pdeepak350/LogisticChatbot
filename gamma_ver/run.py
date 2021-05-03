from Main import app,manager
if __name__ == '__main__':
    app.run(host="127.0.0.1", port='8000',debug=True, use_reloader=False)
    #manager.run()