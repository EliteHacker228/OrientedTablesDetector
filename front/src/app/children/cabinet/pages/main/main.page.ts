import { ChangeDetectionStrategy, ChangeDetectorRef, Component } from '@angular/core';
import { ProcessFileService } from '../../services/process-file.service';
import { ApiService } from '../../../../services/api.service';
import {
    BehaviorSubject,
    catchError,
    delay,
    EMPTY,
    Observable,
    of,
    Subject,
    switchMap,
    take,
    takeUntil,
    tap
} from 'rxjs';

@Component({
    templateUrl: './main.page.html',
    styleUrls: ['./main.page.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush,
    standalone: false
})
export class MainPage {

    public get pageState$(): Observable<PageStateEnum> {
        return this._pageState$.asObservable();
    }

    public file!: Blob;

    private _pageState$: BehaviorSubject<PageStateEnum> = new BehaviorSubject<PageStateEnum>(PageStateEnum.default)
    private _destroyObs: Subject<void> = new Subject();

    constructor(
        private _apiService: ApiService,
        private _cdr: ChangeDetectorRef
    ) {
    }

    public startFileProcess(event: File): void {
        of(null)
            .pipe(
                take(1),
                tap(() => this._pageState$.next(PageStateEnum.process)),
                switchMap(() => this._apiService.fileUpload(event)),
                tap((file: Blob) => {
                    this._pageState$.next(PageStateEnum.success)
                    this.file = file;
                    this._cdr.markForCheck();
                }),
                catchError((err, caught) => {
                    console.log('error');
                    this._pageState$.next(PageStateEnum.error)

                    return EMPTY;
                }),
                takeUntil(this._destroyObs)
            ).subscribe()
    }

    public resetPage(): void {
        this._destroyObs.next()
        this._pageState$.next(PageStateEnum.default)
    }
}

enum PageStateEnum {
    default = 'default' ,
    process = 'process',
    error = 'error',
    success = 'success'
}
