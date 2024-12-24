import { ChangeDetectionStrategy, Component, EventEmitter, Output } from '@angular/core';

@Component({
    selector: 'otd-error',
    templateUrl: './error.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush,
    standalone: false
})
export class ErrorComponent {

    @Output()
    public reset: EventEmitter<any> = new EventEmitter<any>()
}
