// Redux store: legacy createStore wired with the thunk middleware so action
// creators can dispatch async work (API calls).

import { legacy_createStore as createStore, applyMiddleware } from 'redux'
import { thunk } from 'redux-thunk'
import rootReducer from './reducers'

const store = createStore(rootReducer, applyMiddleware(thunk))

export default store
