import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { delay, map, Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class ApiService {
    private _apiUrl = 'http://127.0.0.1:8000';

    constructor(private _http: HttpClient) {}

    public fileUpload(file: File): Observable<Blob> {
        const formData = new FormData();
        formData.append('upload_file', file)

        return this._http.post(`${this._apiUrl}/upload`, formData, {
            responseType: 'blob',
            observe: 'response'
        }).pipe(
            map((response: HttpResponse<any>) => response.body)
        );
    }
}
