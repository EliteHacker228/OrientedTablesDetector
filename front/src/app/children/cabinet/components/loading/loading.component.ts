import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
    selector: 'otd-loading',
    templateUrl: './loading.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush,
    standalone: false
})
export class LoadingComponent {

}
