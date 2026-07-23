import { Link } from 'react-router-dom'
import { useSelector } from 'react-redux'

export default function Header({ title }) {
  const enrolledCourses = useSelector((state) => state.enrollment.enrolledCourses)

  return (
    <>
      <header>
        <h1>{title}</h1>
      </header>

      <nav>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/courses">Courses</Link></li>
          <li><Link to="/profile">Profile ({enrolledCourses.length})</Link></li>
        </ul>
      </nav>
    </>
  )
}
}