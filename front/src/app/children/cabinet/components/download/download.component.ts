import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

@Component({
    selector: 'otd-download',
    templateUrl: './download.component.html',
    styleUrls: ['./download.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush,
    standalone: false
})
export class DownloadComponent {

    @Input()
    public file!: Blob;

    public downloadFile(): void {
        if (!this.file) {
            return;
        }

        const url = window.URL.createObjectURL(this.file);
        const a = document.createElement('a')
        a.href = url;
        a.download = 'processed_img.zip';
        a.click()
    }
}
