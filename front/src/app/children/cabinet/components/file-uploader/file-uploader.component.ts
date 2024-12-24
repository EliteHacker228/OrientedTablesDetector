import { ChangeDetectionStrategy, Component, EventEmitter, Output } from '@angular/core';

@Component({
    selector: 'otb-file-uploader',
    templateUrl: './file-uploader.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush,
    standalone: false
})
export class FileUploaderComponent {

    @Output()
    public fileEmitter: EventEmitter<File> = new EventEmitter<File>();

    public documentUploaded(event: any): void {
        if (event.target.files) {
            this.fileEmitter.emit(event.target.files[0]);
        }
    }
}
