import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Store } from '@ngxs/store';
import { CookieService } from 'ngx-cookie-service';
import { Observable } from 'rxjs';
import { SetActiveUser } from 'src/app/state/actions';
import { IUser } from 'src/app/state/objects';
import { VolatileState } from 'src/app/state/volatile.state';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-appbar',
  templateUrl: './appbar.component.html',
  styleUrls: ['./appbar.component.scss'],
})
export class AppbarComponent {
  public activeUser$: Observable<IUser>;

  constructor(
    private store: Store,
    private cookiesService: CookieService,
    private httpClient: HttpClient
  ) {
    this.activeUser$ = store.select(VolatileState.activeUser);
  }

  public logout() {
    this.httpClient
      .post(`${environment.backendUrl}/auth/logout`, '', { withCredentials: true })
      .subscribe(() => {
        this.cookiesService.delete('token');
        this.store.dispatch(new SetActiveUser(null));
      });
  }
}
