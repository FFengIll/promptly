/* tslint:disable */
/* eslint-disable */
/**
 * FastAPI
 * No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)
 *
 * OpenAPI spec version: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */
/**
 * Intended for use as a base class for externally-facing models.  Any models that inherit from this class will: * accept fields using snake_case or camelCase keys * use camelCase keys in the generated OpenAPI spec * have orm_mode on by default     * Because of this, FastAPI will automatically attempt to parse returned orm instances into the model
 * @export
 * @interface RenameBody
 */
export interface RenameBody {
    /**
     * 
     * @type {string}
     * @memberof RenameBody
     */
    source: string;
    /**
     * 
     * @type {string}
     * @memberof RenameBody
     */
    target: string;
}
