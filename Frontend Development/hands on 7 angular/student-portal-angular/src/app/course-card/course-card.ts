import { Component, Input} from '@angular/core';

@Component({
  selector: 'app-course-card',
   standalone: true,
  imports: [],
  templateUrl: './course-card.html',
  styleUrl: './course-card.css',
})


export class CourseCardComponent {

  @Input() name!: string;

  @Input() code!: string;

  @Input() credits!: number;

  @Input() grade!: string;

}
