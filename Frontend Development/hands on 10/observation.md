/*
NgRx Data Flow

Component
    ↓
dispatch(loadCourses())
    ↓
Effect
    ↓
CourseService API
    ↓
Reducer
    ↓
Store
    ↓
Selector
    ↓
Component Re-renders
*/


# State Management Comparison

| Feature | React + Redux Toolkit | Angular + NgRx | Vue + Pinia |
|---------|------------------------|----------------|-------------|
| Boilerplate | Medium | High | Low |
| Learning Curve | Medium | High | Easy |
| State Updates | Reducers | Reducers | Actions |
| Async Handling | createAsyncThunk | Effects | Async Actions |
| Read State | useSelector | Selectors | storeToRefs |
| Reset State | Custom Reducer | Reducer | $reset() |
| Tooling | Redux DevTools | NgRx DevTools | Vue DevTools |

Summary:

• Redux Toolkit reduces Redux boilerplate using createSlice and createAsyncThunk.
• NgRx follows Redux architecture but separates side effects using Effects.
• Pinia is Vue's official state management library with minimal boilerplate, built-in reactivity, and simpler APIs.