import { useParams } from 'react-router-dom'
import { courses } from '../../public/data.js'

const CourseDetailPage = () => {
  const { courseId } = useParams()
  const course = courses.find((item) => String(item.id) === courseId)

  if (!course) {
    return <p>Course not found.</p>
  }

  return (
    <section>
      <h2>{course.name}</h2>
      <p>Code: {course.code}</p>
      <p>Credits: {course.credits}</p>
      <p>Grade: {course.grade}</p>
    </section>
  )
}

export default CourseDetailPage
