# debate_analysis
## Tips of Deploying app
1.After clonning this git repository, simply direct to the debate_analysis folder

2.Go to the link [https://console.cloud.google.com/project?_ga=1.61127016.593324575.1462282462], and create a new project, set up a project ID

3.type the following command in the terminal  (-A for project ID, -V for version name)
```javascript
appcfg.py -A <YOUR_PROJECT_ID_> -V v1 update pres-debate/
```
4.The app should be deployed and browse at http://YOUR_PROJECT_ID.appspot.com/
