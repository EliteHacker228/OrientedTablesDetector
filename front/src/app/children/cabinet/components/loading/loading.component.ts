import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
    selector: 'otd-loading',
    templateUrl: './loading.component.html',
    styleUrls: ['./loading.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush,
    standalone: false
})
export class LoadingComponent {

}
