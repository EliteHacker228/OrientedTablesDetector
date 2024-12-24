import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
    selector: 'otb-preview',
    templateUrl: './preview.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush,
    standalone: false
})
export class PreviewComponent {

}
