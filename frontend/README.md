# UrbanAI frontend
This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
## Install Instruction
### `npm install`
Resolve the required dependencies from the package.json file.
## Start frontend
### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.
### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)

# Note
You may have the error like this,
```
Error: error:0308010C:digital envelope routines::unsupported
    at new Hash (node:internal/crypto/hash:71:19)
    at Object.createHash (node:crypto:140:10)
    at module.exports (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/util/createHash.js:90:53)
    at NormalModule._initBuildHash (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/NormalModule.js:386:16)
    at handleParseError (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/NormalModule.js:434:10)
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/NormalModule.js:466:5
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/NormalModule.js:327:12
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:373:3
    at iterateNormalLoaders (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:214:10)
    at iterateNormalLoaders (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:221:10)
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:236:3
    at runSyncOrAsync (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:130:11)
    at iterateNormalLoaders (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:232:2)
    at Array.<anonymous> (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:205:4)
    at Storage.finished (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/enhanced-resolve/lib/CachedInputFileSystem.js:55:16)
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/enhanced-resolve/lib/CachedInputFileSystem.js:91:9
/home/shilong/urbanAI/UrbanAI/frontend/node_modules/react-scripts/scripts/start.js:19
  throw err;
  ^

Error: error:0308010C:digital envelope routines::unsupported
    at new Hash (node:internal/crypto/hash:71:19)
    at Object.createHash (node:crypto:140:10)
    at module.exports (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/util/createHash.js:90:53)
    at NormalModule._initBuildHash (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/NormalModule.js:386:16)
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/NormalModule.js:418:10
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/NormalModule.js:293:13
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:367:11
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:233:18
    at context.callback (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:111:13)
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/babel-loader/lib/index.js:51:103 {
  opensslErrorStack: [ 'error:03000086:digital envelope routines::initialization error' ],
  library: 'digital envelope routines',
  reason: 'unsupported',
  code: 'ERR_OSSL_EVP_UNSUPPORTED'
}

```
You can use this command to resolve this problem. Because this problem is due to security issues. 
```bash
export NODE_OPTIONS=--openssl-legacy-provider
```