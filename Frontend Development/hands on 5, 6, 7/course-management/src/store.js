import { configureStore } from '@reduxjs/toolkit'
import enrollmentReducer from './features/enrollment/enrollmentSlice'

export default configureStore({
  reducer: {
    enrollment: enrollmentReducer,
  },
})
