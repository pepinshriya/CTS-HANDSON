import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CourseCardComponent } from '../course-card/course-card';
import { CommonModule } from '@angular/common';
import { CourseService } from '../course.spec';

@Component({
  selector: 'app-course-list',
  standalone: true,
  imports: [FormsModule, CourseCardComponent, CommonModule],
  templateUrl: './course-list.html',
  styleUrl: './course-list.css',
})
export class CourseListComponent implements OnInit {
  constructor(private courseService: CourseService) {}

  courses: any[] = [];
  searchTerm = '';
  loading = false;
  errorMessage = '';

  ngOnInit(): void {

  this.loading = true;

  this.courseService.getCourses().subscribe({

    next: (data) => {

      this.courses = data.map((post, index) => ({
        name: post.title,
        code: `CS10${index + 1}`,
        credits: 4,
        grade: 'A'
      }));

      this.loading = false;
    },

    error: (err) => {

      console.error(err);

      this.errorMessage = 'Unable to load courses. Please try again later.';

      this.loading = false;
    }

  });

}

  get filteredCourses() {
    return this.courses.filter((course) =>
      course.name.toLowerCase().includes(this.searchTerm.toLowerCase()),
    );
  }
}
