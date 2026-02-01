// frontend/assets/js/state/store.js

// Global app state
let state = {
  students: [],
  courses: [],
  enrollments: [],
  editingId: null,
  editingCourseId: null,
};

// Update part of the state
export function setState(newState) {
  state = { ...state, ...newState };
}

// Read the current state
export function getState() {
  return state;
}