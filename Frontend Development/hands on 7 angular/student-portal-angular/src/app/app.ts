import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Header } from './header/header';
import { CourseListComponent } from './course-list/course-list';
import { StudentProfile } from './student-profile/student-profile';

// @Component({
//   selector: 'app-root',
//   standalone: true,
//   imports: [
//     HeaderComponent,
//     CourseListComponent,
//     StudentProfileComponent
//   ],
//   templateUrl: './app.html',
//   styleUrl: './app.css'
// })
// export class App {

// }

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    Header,
        RouterOutlet

    // CourseListComponent,
    // StudentProfile
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('student-portal-angular');
}
