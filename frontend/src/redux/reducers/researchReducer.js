// Reducer holding all research feature state.

import {
  RESEARCH_REQUEST,
  RESEARCH_SUCCESS,
  RESEARCH_FAIL,
  HISTORY_REQUEST,
  HISTORY_SUCCESS,
  HISTORY_FAIL,
  SELECT_RESULT,
} from '../constants/researchConstants'

const initialState = {
  loading: false,
  result: null,
  error: '',
  history: [],
  historyError: '',
}

export default function researchReducer(state = initialState, action) {
  switch (action.type) {
    case RESEARCH_REQUEST:
      return { ...state, loading: true, error: '', result: null }
    case RESEARCH_SUCCESS:
      return { ...state, loading: false, result: action.payload }
    case RESEARCH_FAIL:
      return { ...state, loading: false, error: action.payload }

    case HISTORY_REQUEST:
      return { ...state, historyError: '' }
    case HISTORY_SUCCESS:
      return { ...state, history: action.payload, historyError: '' }
    case HISTORY_FAIL:
      return { ...state, historyError: action.payload }

    case SELECT_RESULT:
      return { ...state, result: action.payload, error: '' }

    default:
      return state
  }
}
