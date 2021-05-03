import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {
  ActivatedRouteSnapshot,
  CanActivate,
  Router,
  RouterStateSnapshot,
  UrlTree,
} from '@angular/router';
import { Store } from '@ngxs/store';
import { CookieService } from 'ngx-cookie-service';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { SetActiveUser } from './state/actions';
import { IUser } from './state/objects';
import { VolatileState } from './state/volatile.state';

@Injectable({ providedIn: 'root' })
export class LoginGuard implements CanActivate {
  constructor(
    private store: Store,
    private cookieService: CookieService,
    private http: HttpClient,
    private router: Router
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean | UrlTree | Observable<boolean | UrlTree> | Promise<boolean | UrlTree> {
    if (state.url === '/login') {
      return this.shouldLogin().then((should) => {
        if (should) {
          return true;
        } else {
          this.router.navigate(['/jobs'], { replaceUrl: true });
        }
      });
    } else {
      return this.shouldLogin().then((should) => {
        if (should) {
          this.router.navigate(['/login'], { replaceUrl: true });
        } else {
          return this.userByToken().then((success) => {
            if (!success) {
              this.router.navigate(['/login'], { replaceUrl: true });
            } else {
              return true;
            }
          });
        }
      });
    }
  }

  private async userByToken(): Promise<boolean> {
    if (this.store.selectSnapshot(VolatileState.activeUser)) {
      return Promise.resolve(true);
    } else {
      return await this.http
        .post<{ user: IUser }>(`${environment.backendUrl}/auth/getCredentialsFromToken`, '', {
          withCredentials: true,
        })
        .pipe(
          map((response) => {
            this.store.dispatch(new SetActiveUser(response.user));
            return response.user != null;
          })
        )
        .toPromise();
    }
  }

  private shouldLogin(): Promise<boolean> {
    const storedUser = this.store.selectSnapshot(VolatileState.activeUser);
    if (storedUser) {
      return Promise.resolve(false);
    } else {
      const token = this.cookieService.get('token');
      if (!token) {
        return Promise.resolve(true);
      } else {
        return this.userByToken().then((success) => !success);
      }
    }
  }
}
