/* tslint:disable */
/* eslint-disable */
/**
 * General Balance
 * customized accounting automation
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


/**
 * * `admin` - Administrator
 * * `member` - Member
 * @export
 */
export const RoleEnum = {
    Admin: 'admin',
    Member: 'member'
} as const;
export type RoleEnum = typeof RoleEnum[keyof typeof RoleEnum];


export function instanceOfRoleEnum(value: any): boolean {
    return Object.values(RoleEnum).includes(value);
}

export function RoleEnumFromJSON(json: any): RoleEnum {
    return RoleEnumFromJSONTyped(json, false);
}

export function RoleEnumFromJSONTyped(json: any, ignoreDiscriminator: boolean): RoleEnum {
    return json as RoleEnum;
}

export function RoleEnumToJSON(value?: RoleEnum | null): any {
    return value as any;
}

