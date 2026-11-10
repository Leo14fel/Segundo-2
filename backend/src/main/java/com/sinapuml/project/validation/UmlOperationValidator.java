package com.sinapuml.project.validation;
import com.sinapuml.project.domain.document.*;
import java.util.*;
import java.util.regex.Pattern;
final class UmlOperationValidator {
 private static final Pattern NAME=Pattern.compile("[A-Za-z_][A-Za-z0-9_]*");
 private static final Pattern TYPE=Pattern.compile("[A-Za-z_][A-Za-z0-9_]*(?:\\[\\])?");
 void validate(List<UmlClass> classes, ProjectValidationCollector c){
  Set<UUID> ids=new HashSet<>();
  for(var owner:classes){if(owner==null)continue; if(owner.id()!=null)ids.add(owner.id());for(var a:owner.attributes())if(a!=null&&a.id()!=null)ids.add(a.id());}
  for(int i=0;i<classes.size();i++){var owner=classes.get(i);if(owner==null)continue;Set<String> signatures=new HashSet<>();
   for(int j=0;j<owner.operations().size();j++){var op=owner.operations().get(j);String path="document.umlModel.classes["+i+"].operations["+j+"]";
    if(op==null){c.error(path,"OPERATION_REQUIRED",owner.id(),"El método no puede ser nulo.");continue;}
    identity(op.id(),path,ids,owner.id(),c);name(op.name(),path+".name",owner.id(),c);
    if(op.visibility()==null)c.error(path+".visibility","OPERATION_VISIBILITY_REQUIRED",op.id(),"Selecciona la visibilidad del método.");
    if(op.returnType()!=null&&!op.returnType().isBlank()&&!op.returnType().equalsIgnoreCase("void"))type(op.returnType(),path+".returnType",op.id(),c);
    Set<String> names=new HashSet<>();List<String> types=new ArrayList<>();
    for(int k=0;k<op.parameters().size();k++){var param=op.parameters().get(k);String pp=path+".parameters["+k+"]";
     if(param==null){c.error(pp,"PARAMETER_REQUIRED",op.id(),"El parámetro no puede ser nulo.");continue;}
     identity(param.id(),pp,ids,op.id(),c);name(param.name(),pp+".name",op.id(),c);type(param.type(),pp+".type",op.id(),c);
     if(param.name()!=null&&!names.add(param.name().toLowerCase(Locale.ROOT)))c.error(pp,"DUPLICATE_PARAMETER_NAME",op.id(),"El nombre del parámetro está repetido.");
     types.add(param.type()==null?"":param.type().toUpperCase(Locale.ROOT));
    }
    String signature=op.name()+"("+String.join(",",types)+")";
    if(!signatures.add(signature))c.error(path,"DUPLICATE_OPERATION_SIGNATURE",op.id(),"Ya existe un método con el mismo nombre y tipos de parámetros.");
   }
  }
 }
 private void identity(UUID id,String path,Set<UUID> ids,UUID owner,ProjectValidationCollector c){if(id==null)c.error(path+".id","OPERATION_MEMBER_ID_REQUIRED",owner,"El miembro necesita un identificador.");else if(!ids.add(id))c.error(path+".id","DUPLICATE_OPERATION_MEMBER_ID",id,"El identificador del miembro está repetido.");}
 private void name(String value,String path,UUID id,ProjectValidationCollector c){if(value==null||value.length()>80||!NAME.matcher(value).matches())c.error(path,"OPERATION_NAME_INVALID",id,"Usa un nombre de código de hasta 80 caracteres.");}
 private void type(String value,String path,UUID id,ProjectValidationCollector c){if(value==null||value.length()>120||!TYPE.matcher(value).matches()||value.equalsIgnoreCase("void"))c.error(path,"OPERATION_TYPE_INVALID",id,"Selecciona un tipo simple o arreglo válido; void solo se admite como retorno.");}
}
