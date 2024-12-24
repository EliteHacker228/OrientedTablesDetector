import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { MainPage } from './pages/main/main.page';
import { LoadingComponent } from './components/loading/loading.component';
import { ErrorComponent } from './components/error/error.component';
import { PreviewComponent } from './components/preview/preview.component';
import { DownloadComponent } from './components/download/download.component';
import { ProcessFileService } from './services/process-file.service';
import { FileUploaderComponent } from './components/file-uploader/file-uploader.component';

const routes: Routes = [
    {
        path: '',
        component: MainPage,
    }
];

@NgModule({
    imports: [
        CommonModule,
        RouterModule.forChild(routes)
    ],
    declarations: [
        MainPage,
        LoadingComponent,
        ErrorComponent,
        PreviewComponent,
        DownloadComponent,
        FileUploaderComponent
    ],
    providers: [
        ProcessFileService
    ]
})
export class CabinetModule {

}
