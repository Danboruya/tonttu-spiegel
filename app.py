import bottle
import routes
import subprocess

app = routes.app

if __name__ == '__main__':
    # subprocess.Popen(["python ./assistant.py", "--project-id", "hucis-lab-assistant-actionssdk", "--devi-model-id",
    #                  "hucis-lab-assistant-actionssdk-geneal-p27hip"], shell=True)
    bottle.run(app=app, host='0.0.0.0', port=8080, reloader=True, debug=True)
