// Action creators (thunks) for the research feature.
// These call the API service layer in ../../api and dispatch results.

import { research, getHistory } from '../../api'
import {
  RESEARCH_REQUEST,
  RESEARCH_SUCCESS,
  RESEARCH_FAIL,
  HISTORY_REQUEST,
  HISTORY_SUCCESS,
  HISTORY_FAIL,
  SELECT_RESULT,
} from '../constants/researchConstants'

/** Load past research queries into the store. */
export const fetchHistory = () => async (dispatch) => {
  dispatch({ type: HISTORY_REQUEST })
  try {
    const items = await getHistory()
    dispatch({ type: HISTORY_SUCCESS, payload: items })
  } catch {
    dispatch({
      type: HISTORY_FAIL,
      payload: "Couldn't load history. Is the backend running?",
    })
  }
}

/** Ask the agent a question, store the result, then refresh history. */
export const runResearch = (query) => async (dispatch) => {
  dispatch({ type: RESEARCH_REQUEST })
  try {
    const result = await research(query)
    dispatch({ type: RESEARCH_SUCCESS, payload: result })
    dispatch(fetchHistory())
  } catch (err) {
    dispatch({
      type: RESEARCH_FAIL,
      payload: err instanceof Error ? err.message : 'Something went wrong.',
    })
  }
}

/** Show a stored result (e.g. clicked from history) without a new request. */
export const selectResult = (result) => ({
  type: SELECT_RESULT,
  payload: result,
})
