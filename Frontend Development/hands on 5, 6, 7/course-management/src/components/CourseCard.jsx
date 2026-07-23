import { useDispatch } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { enroll } from '../features/enrollment/enrollmentSlice'

const CourseCard = ({ course }) => {
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const handleEnroll = (event) => {
    event.stopPropagation()
    dispatch(enroll(course))
    navigate('/profile')
  }

  const handleViewDetails = (event) => {
    event.stopPropagation()
    navigate(`/courses/${course.id}`)
  }

  return (
    <div onClick={() => navigate(`/courses/${course.id}`)} style={{ border: '1px solid #ccc', margin: '1rem 0', padding: '1rem' }}>
      <h3>{course.name}</h3>
      <p>Credits: {course.credits}</p>
      <p>Grade: {course.grade}</p>
      <p>Code: {course.code}</p>
      <button type="button" onClick={handleEnroll}>Enroll</button>
      <button type="button" onClick={handleViewDetails} style={{ marginLeft: '0.5rem' }}>View Details</button>
    </div>
  )
}

export default CourseCard
