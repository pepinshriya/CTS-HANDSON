import { useDispatch, useSelector } from 'react-redux'
import { unenroll } from '../features/enrollment/enrollmentSlice'

const ProfilePage = () => {
  const enrolledCourses = useSelector((state) => state.enrollment.enrolledCourses)
  const dispatch = useDispatch()

  return (
    <section>
      <h2>Your Profile</h2>
      {enrolledCourses.length === 0 ? (
        <p>No courses enrolled yet.</p>
      ) : (
        <ul>
          {enrolledCourses.map((course) => (
            <li key={course.id}>
              {course.name} ({course.code})
              <button
                type="button"
                onClick={() => dispatch(unenroll(course.id))}
                style={{ marginLeft: '0.5rem' }}
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}

export default ProfilePage
